"""Asynchronous task support for animating lights."""

import asyncio
from collections.abc import Awaitable
from functools import cached_property


class TaskableMixin:
    """Associate and manage asynchronous tasks.

    Tasks can be added and cancelled.
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
        """Active tasks that are associated with this class."""
        return {}

    def add_task(self, name: str, coroutine: Awaitable) -> asyncio.Task:
        """Create a new task using coroutine as the body and stash it in the tasks dict.

        Using name as a key for the tasks dictionary.

        :name: str
        :coroutine: Awaitable
        :return: asyncio.Task
        """
        try:
            return self.tasks[name]
        except KeyError:
            pass

        # >py3.7, create_task takes a `name` parameter
        self.tasks[name] = self.event_loop.create_task(coroutine(self))

        return self.tasks[name]

    def cancel_task(self, name: str) -> asyncio.Task | None:
        """Cancel a task associated with name if it exists.

        If the task exists the cancelled task is returned, otherwise None.

        :name: str
        :return: None | asyncio.Task
        """
        try:
            task = self.tasks[name]
            del self.tasks[name]
            task.cancel()
        except (KeyError, AttributeError):
            pass
        else:
            return task

        return None

    def cancel_tasks(self) -> None:
        """Cancel all tasks and return nothing."""
        for task in self.tasks.values():
            task.cancel()
        self.tasks.clear()
