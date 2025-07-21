"""Asynchronous task support for animating lights."""

import asyncio
import time
from collections.abc import Awaitable
from dataclasses import dataclass
from enum import IntEnum
from functools import cached_property
from typing import Any

from loguru import logger


class TaskPriority(IntEnum):
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class TaskInfo:
    task: asyncio.Task
    priority: TaskPriority
    name: str
    created_at: float
    
    @property
    def is_running(self) -> bool:
        return not self.task.done()
    
    @property
    def is_cancelled(self) -> bool:
        return self.task.cancelled()
    
    @property
    def has_exception(self) -> bool:
        return self.task.done() and not self.task.cancelled() and self.task.exception() is not None
    
    @property
    def exception(self) -> BaseException | None:
        if self.has_exception:
            return self.task.exception()
        return None


class TaskableMixin:
    """Associate and manage asynchronous tasks."""

    @cached_property
    def event_loop(self) -> asyncio.AbstractEventLoop:
        try:
            return asyncio.get_running_loop()
        except RuntimeError:
            return asyncio.new_event_loop()

    @cached_property
    def tasks(self) -> dict[str, asyncio.Task]:
        return {}
    
    @cached_property
    def task_info(self) -> dict[str, TaskInfo]:
        return {}

    def add_task(
        self, 
        name: str, 
        coroutine: Awaitable, 
        priority: TaskPriority = TaskPriority.NORMAL,
        replace: bool = False
    ) -> asyncio.Task:
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
            task=task,
            priority=priority,
            name=name,
            created_at=time.time()
        )
        self.task_info[name] = task_info
        self.tasks[name] = task
        
        task.add_done_callback(self._task_completion_callback)
        return task

    def cancel_task(self, name: str) -> asyncio.Task | None:
        try:
            task = self.tasks[name]
            del self.tasks[name]
            if name in self.task_info:
                del self.task_info[name]
            
            try:
                task.cancel()
                return task
            except AttributeError:
                return None
                
        except KeyError:
            pass
        
        return None

    def cancel_tasks(self, priority: TaskPriority | None = None) -> None:
        if priority is None:
            for task in self.tasks.values():
                task.cancel()
            self.tasks.clear()
            self.task_info.clear()
        else:
            to_cancel = [
                name for name, task_info in self.task_info.items()
                if task_info.priority == priority and task_info.is_running
            ]
            for name in to_cancel:
                self.task_info[name].task.cancel()
            self._cleanup_completed_tasks()
    
    def get_task_status(self, name: str) -> dict[str, Any] | None:
        task_info = self.task_info.get(name)
        if not task_info:
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
        active = []
        for name, task_info in self.task_info.items():
            if task_info.is_running:
                active.append(name)
        
        for name, task in self.tasks.items():
            if name not in self.task_info and not task.done():
                active.append(name)
        
        return sorted(active)
    
    def _cleanup_completed_tasks(self) -> None:
        completed = [
            name for name, task_info in self.task_info.items() 
            if not task_info.is_running
        ]
        for name in completed:
            del self.task_info[name]
        
        completed_tasks = []
        for name, task in self.tasks.items():
            try:
                if isinstance(task, asyncio.Task) and task.done():
                    completed_tasks.append(name)
            except (AttributeError, TypeError):
                pass
        
        for name in completed_tasks:
            del self.tasks[name]
    
    def _task_completion_callback(self, task: asyncio.Task) -> None:
        try:
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
                logger.error(f"Task '{task_name}' failed: {task.exception()}")
            else:
                logger.debug(f"Task '{task_name}' completed successfully")
                
        except Exception as e:
            logger.error(f"Error in task completion callback: {e}")