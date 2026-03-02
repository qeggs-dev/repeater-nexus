import time
import traceback

from ._resource import Resource
from datetime import datetime
from fastapi import Request
from fastapi.responses import Response, ORJSONResponse
from typing import Callable, Awaitable
from loguru import logger

@Resource.app.middleware("http")
async def except_catcher(request: Request, call_next: Callable[[Request], Awaitable[Response]]):
    try:
        response: Response = await call_next(request)
        return response
    except Exception as e:
        now = time.time_ns()
        now_datetime = datetime.fromtimestamp(now / 1e9) # POSIX timestamp to datetime
        logger.exception(
            "Error {error}\n{traceback}",
            error = str(e),
            traceback = traceback.format_exc(),
        )
        return ORJSONResponse(
            status_code=500,
            content={
                "error": str(e),
                "posix_time": now_datetime.timestamp(), # POSIX timestamp
                "iso_time": now_datetime.isoformat(), # ISO 8601 timeformat
                "time_ns": now, # nanoseconds since epoch
                "time": now // 1_000_000_000 # seconds since epoch
            },
            media_type="text/plain"
        )