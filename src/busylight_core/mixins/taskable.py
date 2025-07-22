"""Asynchronous task support for animating lights."""

import asyncio
import contextlib
import time
from collections.abc import Awaitable
from dataclasses import dataclass
from enum import IntEnum
from functools import cached_property
from typing import Any

from loguru import logger


class TaskPriority(IntEnum):
    """Task priority levels for scheduling.

    Used to control task execution priority and enable priority-based
    cancellation of tasks.
    """

    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class TaskInfo:
    """Information about a managed task.

    Contains task metadata including priority, creation time, and status
    information for enhanced task monitoring and debugging.
    """

    task: asyncio.Task
    priority: TaskPriority
    name: str
    created_at: float

    @property
    def is_running(self) -> bool:
        """Check if task is currently running.

        Returns True if the task has not completed, been cancelled, or failed.
        """
        return not self.task.done()

    @property
    def is_cancelled(self) -> bool:
        """Check if task was cancelled.

        Returns True if the task was explicitly cancelled before completion.
        """
        return self.task.cancelled()

    @property
    def has_exception(self) -> bool:
        """Check if task completed with an exception.

        Returns True if the task completed but raised an unhandled exception.
        """
        return (
            self.task.done()
            and not self.task.cancelled()
            and self.task.exception() is not None
        )

    @property
    def exception(self) -> BaseException | None:
        """Get task exception if any.

        Returns the exception that caused the task to fail, or None if
        the task completed successfully or is still running.
        """
        if self.has_exception:
            return self.task.exception()
        return None


class TaskableMixin:
    """Associate and manage asynchronous tasks.

    Provides enhanced task management with prioritization, error handling,
    and task monitoring capabilities for Light instances.
    """

    @cached_property
    def event_loop(self) -> asyncio.AbstractEventLoop:
        """The default event loop.

        Returns the currently running event loop, or creates a new one if
        no event loop is currently running.
        """
        try:
            return asyncio.get_running_loop()
        except RuntimeError:
            return asyncio.new_event_loop()

    @cached_property
    def tasks(self) -> dict[str, asyncio.Task]:
        """Active tasks that are associated with this instance.

        Dictionary mapping task names to their corresponding asyncio.Task objects.
        """
        return {}

    @cached_property
    def task_info(self) -> dict[str, TaskInfo]:
        """Enhanced task information with priority and status tracking.

        Dictionary mapping task names to TaskInfo objects containing metadata
        about priority, creation time, and current status.
        """
        return {}

    def add_task(
        self,
        name: str,
        coroutine: Awaitable,
        priority: TaskPriority = TaskPriority.NORMAL,
        replace: bool = False,
    ) -> asyncio.Task:
        """Create a new task using coroutine as the body and stash it in the tasks dict.

        Creates and manages an asyncio task with enhanced tracking and error handling.

        :param name: Unique identifier for the task
        :param coroutine: Awaitable function to run as task
        :param priority: Task priority level for scheduling
        :param replace: Whether to replace existing task with same name
        :return: The created or existing asyncio.Task
        """
        self._cleanup_completed_tasks()

        if not replace:
            existing_task = self.tasks.get(name)
            if existing_task:
                return existing_task
        else:
            existing = self.task_info.get(name)
            if existing:
                existing.task.cancel()
                del self.task_info[name]
                del self.tasks[name]

        task = self.event_loop.create_task(coroutine(self), name=name)

        task_info = TaskInfo(
            task=task, priority=priority, name=name, created_at=time.time()
        )
        self.task_info[name] = task_info
        self.tasks[name] = task

        task.add_done_callback(self._task_completion_callback)
        return task

    def cancel_task(self, name: str) -> asyncio.Task | None:
        """Cancel a task associated with name if it exists.

        Removes the task from tracking and attempts to cancel it.

        :param name: Name of task to cancel
        :return: The cancelled task or None if not found
        """
        with contextlib.suppress(KeyError):
            task = self.tasks[name]
            del self.tasks[name]
            if name in self.task_info:
                del self.task_info[name]

            with contextlib.suppress(AttributeError):
                task.cancel()
                return task

        return None

    def cancel_tasks(self, priority: TaskPriority | None = None) -> None:
        """Cancel all tasks or tasks of specific priority.

        Cancels either all tasks or only tasks matching the specified priority level.

        :param priority: If specified, only cancel tasks of this priority level
        """
        if priority is None:
            for task in self.tasks.values():
                task.cancel()
            self.tasks.clear()
            self.task_info.clear()
        else:
            to_cancel = [
                name
                for name, task_info in self.task_info.items()
                if task_info.priority == priority and task_info.is_running
            ]
            for name in to_cancel:
                self.task_info[name].task.cancel()
            self._cleanup_completed_tasks()

    def get_task_status(self, name: str) -> dict[str, Any] | None:
        """Get detailed status information for a task.

        Returns comprehensive status information including running state,
        exceptions, priority, and creation time.

        :param name: Name of task to check
        :return: Dictionary with task status details or None if not found
        """
        task_info = self.task_info.get(name)
        if not task_info:
            task = self.tasks.get(name)
            if task:
                return {
                    "name": name,
                    "running": not task.done(),
                    "cancelled": task.cancelled(),
                    "has_exception": task.done()
                    and not task.cancelled()
                    and task.exception() is not None,
                    "exception": task.exception() if task.done() else None,
                    "priority": "unknown",
                    "created_at": "unknown",
                }
            return None

        return {
            "name": task_info.name,
            "running": task_info.is_running,
            "cancelled": task_info.is_cancelled,
            "has_exception": task_info.has_exception,
            "exception": task_info.exception,
            "priority": task_info.priority.name,
            "created_at": task_info.created_at,
        }

    def list_active_tasks(self) -> list[str]:
        """Get list of currently active task names.

        Returns sorted list of task names that are currently running.

        :return: List of task names that are currently running
        """
        active = []
        for name, task_info in self.task_info.items():
            if task_info.is_running:
                active.append(name)

        for name, task in self.tasks.items():
            if name not in self.task_info and not task.done():
                active.append(name)

        return sorted(active)

    def _cleanup_completed_tasks(self) -> None:
        """Remove completed tasks from tracking dictionaries.

        Internal method to clean up task dictionaries by removing references
        to completed, cancelled, or failed tasks.
        """
        completed = [
            name
            for name, task_info in self.task_info.items()
            if not task_info.is_running
        ]
        for name in completed:
            del self.task_info[name]

        completed_tasks = []
        for name, task in self.tasks.items():
            with contextlib.suppress(AttributeError, TypeError):
                if isinstance(task, asyncio.Task) and task.done():
                    completed_tasks.append(name)

        for name in completed_tasks:
            del self.tasks[name]

    def _task_completion_callback(self, task: asyncio.Task) -> None:
        """Handle task completion for error monitoring.

        Internal callback that logs task completion, cancellation, or failure
        for debugging and monitoring purposes.

        :param task: The completed task
        """
        try:
            task_name = "unknown"

            for name, info in self.task_info.items():
                if info.task is task:
                    task_name = name
                    break
            else:
                logger.debug("Task {task} not found.")
                return

            if task.cancelled():
                logger.debug(f"Task '{task_name}' was cancelled")
                return

            if task.exception():
                logger.error(f"Task '{task_name}' failed: {task.exception()}")
                return

            logger.debug(f"Task '{task_name}' completed successfully")

        except Exception as error:
            logger.error(f"Error in task completion callback: {error}")
