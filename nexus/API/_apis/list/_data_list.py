import orjson

from uuid import UUID
from fastapi.responses import ORJSONResponse, StreamingResponse
from loguru import logger

from ..._resource import Resource
from ....Global_Config import GlobalConfigManager
from ....Storage import Storage

@Resource.app.get("/api/{pool}/resources/{resource_id}/datas")
async def data_list(pool: str, resource_id: str):
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
    
    try:
        uuid = UUID(resource_id)
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
        content = list(storage.datas(resource_id))
    )

@Resource.app.get("/api/{pool}/resources/{resource_id}/datas/stream")
async def data_list_stream(pool: str, resource_id: str):
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
        content = (orjson.dumps(id) for id in storage.datas(resource_id)),
        media_type = "application/x-ndjson"
    )