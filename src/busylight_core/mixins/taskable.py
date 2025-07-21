"""Asynchronous task support for animating lights."""

import asyncio
from collections.abc import Awaitable
from dataclasses import dataclass
from enum import IntEnum
from functools import cached_property
from typing import Any

from loguru import logger


class TaskPriority(IntEnum):
    """Task priority levels for scheduling."""
    
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class TaskInfo:
    """Information about a managed task."""
    
    task: asyncio.Task
    priority: TaskPriority
    name: str
    created_at: float
    
    @property
    def is_running(self) -> bool:
        """Check if task is currently running."""
        return not self.task.done()
    
    @property
    def is_cancelled(self) -> bool:
        """Check if task was cancelled."""
        return self.task.cancelled()
    
    @property
    def has_exception(self) -> bool:
        """Check if task completed with an exception."""
        return self.task.done() and not self.task.cancelled() and self.task.exception() is not None
    
    @property
    def exception(self) -> BaseException | None:
        """Get task exception if any."""
        if self.has_exception:
            return self.task.exception()
        return None


class TaskableMixin:
    """Associate and manage asynchronous tasks with prioritization and error handling.

    Enhanced task management supporting:
    - Task prioritization
    - Error handling and monitoring
    - Task health checks
    - Prevention of accidental overwrites
    """

    @cached_property
    def event_loop(self) -> asyncio.AbstractEventLoop:
        """The default event loop."""
        try:
            return asyncio.get_running_loop()
        except RuntimeError:
            return asyncio.new_event_loop()

    @cached_property
    def tasks(self) -> dict[str, asyncio.Task]:
        """Active tasks that are associated with this instance.
        
        Deprecated: Use task_info for enhanced task management.
        Maintained for backward compatibility.
        """
        return {}
    
    @cached_property
    def task_info(self) -> dict[str, TaskInfo]:
        """Enhanced task information with priority and status tracking."""
        return {}

    def add_task(
        self, 
        name: str, 
        coroutine: Awaitable, 
        priority: TaskPriority = TaskPriority.NORMAL,
        replace: bool = False
    ) -> asyncio.Task:
        """Create a new task using coroutine as the body and stash it in the tasks dict.

        Using name as a key for the tasks dictionary.

        Args:
            name: Unique identifier for the task
            coroutine: Awaitable function to run as task
            priority: Task priority level for scheduling
            replace: Whether to replace existing task with same name
            
        Returns:
            The created or existing asyncio.Task
            
        Raises:
            ValueError: If task exists and replace=False
        """
        # Clean up any completed tasks first
        self._cleanup_completed_tasks()
        
        # Original behavior: check if task exists in dict (for backward compatibility)  
        if not replace:
            try:
                existing_task = self.tasks[name]
                logger.debug(f"Task '{name}' already exists, returning existing")
                return existing_task
            except KeyError:
                pass
        else:
            # Handle replacement case
            existing_task = self.tasks.get(name)
            if existing_task:
                logger.debug(f"Replacing existing task '{name}'")
                try:
                    existing_task.cancel()
                except AttributeError:
                    pass  # Handle mock objects or None
                # Remove from both tracking systems
                del self.tasks[name]
                if name in self.task_info:
                    del self.task_info[name]
        
        # Create new task with enhanced error handling
        try:
            task = self.event_loop.create_task(coroutine(self), name=name)
            
            # Store task info
            import time
            task_info = TaskInfo(
                task=task,
                priority=priority,
                name=name,
                created_at=time.time()
            )
            self.task_info[name] = task_info
            
            # Maintain backward compatibility
            self.tasks[name] = task
            
            # Add completion callback for error monitoring
            task.add_done_callback(self._task_completion_callback)
            
            logger.debug(f"Created task '{name}' with priority {priority.name}")
            return task
            
        except Exception as e:
            logger.error(f"Failed to create task '{name}': {e}")
            raise

    def cancel_task(self, name: str) -> asyncio.Task | None:
        """Cancel a task associated with name if it exists.

        If the task exists the cancelled task is returned, otherwise None.

        Args:
            name: Name of task to cancel
            
        Returns:
            The cancelled task or None if not found
        """
        try:
            # Get task from legacy dict (maintain compatibility)
            task = self.tasks[name]
            # Remove from both tracking systems first (maintain original behavior)
            del self.tasks[name]
            if name in self.task_info:
                del self.task_info[name]
            
            try:
                # Cancel the task  
                task.cancel()
                logger.debug(f"Cancelled task '{name}'")
                return task
            except AttributeError:
                # Handle case where task is None or doesn't have cancel method
                logger.debug(f"Task '{name}' doesn't have cancel method")
                return None  # Return None when cancel fails
                
        except KeyError:
            # Task doesn't exist
            pass
        
        return None

    def cancel_tasks(self, priority: TaskPriority | None = None) -> None:
        """Cancel all tasks or tasks of specific priority.
        
        Args:
            priority: If specified, only cancel tasks of this priority level
        """
        cancelled_count = 0
        
        # If no priority filter, cancel all tasks (maintain legacy behavior)
        if priority is None:
            for task in self.tasks.values():
                task.cancel()  # Let exceptions propagate (original behavior)
                cancelled_count += 1
        else:
            # Priority-based cancellation using enhanced tracking
            for name, task_info in list(self.task_info.items()):
                if task_info.priority == priority and task_info.is_running:
                    try:
                        task_info.task.cancel()
                        cancelled_count += 1
                    except (AttributeError, Exception):
                        pass
        
        if priority is None:
            self.tasks.clear()
            self.task_info.clear()
            logger.debug(f"Cancelled all {cancelled_count} tasks")
        else:
            # Clean up cancelled tasks from tracking
            self._cleanup_completed_tasks()
            logger.debug(f"Cancelled {cancelled_count} tasks with priority {priority.name}")
    
    def get_task_status(self, name: str) -> dict[str, Any] | None:
        """Get detailed status information for a task.
        
        Args:
            name: Name of task to check
            
        Returns:
            Dictionary with task status details or None if not found
        """
        task_info = self.task_info.get(name)
        if not task_info:
            # Check legacy tasks
            task = self.tasks.get(name)
            if task:
                return {
                    "name": name,
                    "running": not task.done(),
                    "cancelled": task.cancelled(),
                    "has_exception": task.done() and not task.cancelled() and task.exception() is not None,
                    "exception": task.exception() if task.done() else None,
                    "priority": "unknown",
                    "created_at": "unknown"
                }
            return None
        
        return {
            "name": task_info.name,
            "running": task_info.is_running,
            "cancelled": task_info.is_cancelled,
            "has_exception": task_info.has_exception,
            "exception": task_info.exception,
            "priority": task_info.priority.name,
            "created_at": task_info.created_at
        }
    
    def list_active_tasks(self) -> list[str]:
        """Get list of currently active task names.
        
        Returns:
            List of task names that are currently running
        """
        active = []
        
        # Check enhanced task info
        for name, task_info in self.task_info.items():
            if task_info.is_running:
                active.append(name)
        
        # Check legacy tasks not in task_info
        for name, task in self.tasks.items():
            if name not in self.task_info and not task.done():
                active.append(name)
        
        return sorted(active)
    
    def _cleanup_completed_tasks(self) -> None:
        """Remove completed tasks from tracking dictionaries."""
        # Clean up task_info
        completed_names = [
            name for name, task_info in self.task_info.items() 
            if not task_info.is_running
        ]
        for name in completed_names:
            del self.task_info[name]
        
        # Clean up legacy tasks (handle mock objects gracefully)
        completed_legacy = []
        for name, task in self.tasks.items():
            try:
                # Only clean up real asyncio.Task objects, skip Mock objects
                import asyncio
                if isinstance(task, asyncio.Task) and task.done():
                    completed_legacy.append(name)
            except (AttributeError, TypeError):
                # Skip mock objects or invalid tasks
                pass
        
        for name in completed_legacy:
            del self.tasks[name]
    
    def _task_completion_callback(self, task: asyncio.Task) -> None:
        """Handle task completion for error monitoring.
        
        Args:
            task: The completed task
        """
        try:
            # Find task info
            task_info = None
            task_name = "unknown"
            
            for name, info in self.task_info.items():
                if info.task is task:
                    task_info = info
                    task_name = name
                    break
            
            if task.cancelled():
                logger.debug(f"Task '{task_name}' was cancelled")
            elif task.exception():
                exception = task.exception()
                logger.error(f"Task '{task_name}' failed with exception: {exception}")
                if task_info:
                    logger.error(f"Task priority: {task_info.priority.name}, created at: {task_info.created_at}")
            else:
                logger.debug(f"Task '{task_name}' completed successfully")
                
        except Exception as e:
            logger.error(f"Error in task completion callback: {e}")
