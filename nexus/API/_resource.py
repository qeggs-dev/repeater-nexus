import uvicorn

from typing import Any, Callable, ClassVar, Sequence
from fastapi import FastAPI
from ._warning_catcher import WarningHandler
from ..Delayed_Tasks_Pool import DelayedTasksPool
from ..Lifespan import ExitHandler
from ._lifespan import lifespan
from .._info import __version__

class Resource:
    startup: ClassVar[Sequence[Callable[[], Any]] | None] = None
    shutdown: ClassVar[Sequence[Callable[[], Any]] | None] = None

    app: ClassVar[FastAPI] = FastAPI(
        title = "Repeater_Nexus",
        lifespan = lifespan,
        on_startup = startup,
        on_shutdown = shutdown,
        version = __version__
    )

    delayed_tasks_pool: ClassVar[DelayedTasksPool] = DelayedTasksPool()
    warning_handler: ClassVar[WarningHandler] = WarningHandler()

    @classmethod
    def init_delayed_task_pool(cls) -> None:
        ExitHandler.add_function(
            cls.delayed_tasks_pool.cancel_all(wait = True)
        )
    
    @classmethod
    def init_warning_catcher(cls) -> None:
        cls.warning_handler.inject()
    
    @classmethod
    def init_all(cls) -> None:
        cls.init_delayed_task_pool()
        cls.init_warning_catcher()

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