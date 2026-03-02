import orjson

from fastapi.responses import ORJSONResponse
from loguru import logger
from uuid import UUID

from ..._resource import Resource
from ....Global_Config import GlobalConfigManager
from ....Storage import Storage
from ._response import DownloadResponse

@Resource.app.get("/api/{pool}/download/{resources_id}/{data_id}")
async def download_json(pool: str, resources_id: str, data_id: str):
    path = GlobalConfigManager.get_configs().storage.storage_path
    suffix = GlobalConfigManager.get_configs().storage.file_suffix
    try:
        storage = Storage(path, pool)
    except ValueError as e:
        return ORJSONResponse(
            DownloadResponse(
                status = "error",
                message = str(e)
            ).model_dump(exclude_none=True),
            status_code = 400
        )
    try:
        file_uuid = UUID(resources_id)
    except ValueError:
        return ORJSONResponse(
            DownloadResponse(
                status = "error",
                message = "Invalid file id"
            ).model_dump(exclude_none=True),
            status_code=400
        )
    
    if not storage.data_exists(file_uuid, data_id):
        return ORJSONResponse(
            DownloadResponse(
                status = "error",
                message = "File not found"
            ).model_dump(exclude_none=True),
            status_code=404
        )
    

    try:
        data = await storage.load(file_uuid, data_id)
    except orjson.JSONDecodeError:
        logger.error(
            "Failed to decode file {resource_id}/{data_id}",
            resource_id = resources_id,
            data_id = data_id
        )
        return ORJSONResponse(
            DownloadResponse(
                status = "error",
                message = "Failed to decode file"
            ).model_dump(exclude_none=True),
            status_code=500
        )

    return ORJSONResponse(
        DownloadResponse(
            status = "success",
            message = "File loaded",
            data = data
        ).model_dump(exclude_none=True),
        status_code=200
    )