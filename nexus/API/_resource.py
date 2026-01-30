import uvicorn

from typing import Any, Callable, ClassVar, Sequence
from fastapi import FastAPI
from ..Delayed_Tasks_Pool import DelayedTasksPool
from ._lifespan import lifespan
from .._info import __version__

class Resource:
    startup: ClassVar[Sequence[Callable[[], Any]] | None] = None
    shutdown: ClassVar[Sequence[Callable[[], Any]] | None] = None

    app: ClassVar[FastAPI] = FastAPI(
        title = "RepeaterChatBackend",
        lifespan = lifespan,
        on_startup = startup,
        on_shutdown = shutdown,
        version = __version__
    )

    delayed_tasks_pool: ClassVar[DelayedTasksPool] = DelayedTasksPool()

    @classmethod
    def run(
            cls,
            host: str = "0.0.0.0",
            port: int = 8000,
            reload: bool = False,
            workers: int | None = None
        ):
        """Run the FastAPI app."""
        uvicorn.run(
            app = cls.app,
            host = host,
            port = port,
            reload = reload,
            workers = workers,
            log_config = None,
        )