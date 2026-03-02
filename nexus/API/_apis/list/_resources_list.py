import orjson

from fastapi.responses import ORJSONResponse, StreamingResponse
from loguru import logger

from ..._resource import Resource
from ....Global_Config import GlobalConfigManager
from ....Storage import Storage

@Resource.app.get("/api/{pool}/resources_list")
async def resources_list(pool: str):
    path = GlobalConfigManager.get_configs().storage.storage_path
    try:
        storage = Storage(path, pool)
    except ValueError as e:
        return ORJSONResponse(
            status_code = 404,
            content = {
                "error": str(e)
            }
        )
    logger.info(
        "Getting file list"
    )
    return ORJSONResponse(
        content = storage.filelist()
    )

@Resource.app.get("/api/{pool}/resources_list/stream")
async def resources_list_stream(pool: str):
    path = GlobalConfigManager.get_configs().storage.storage_path
    try:
        storage = Storage(path, pool)
    except ValueError as e:
        return ORJSONResponse(
            status_code = 404,
            content = {
                "error": str(e)
            }
        )
    logger.info(
        "Getting file list"
    )
    
    return StreamingResponse(
        content = (orjson.dumps(id) for id in storage.resources()),
        media_type = "application/x-ndjson"
    )