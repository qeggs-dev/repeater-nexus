import orjson

from fastapi.responses import ORJSONResponse
from loguru import logger
from uuid import UUID

from ..._resource import Resource
from ....Global_Config import GlobalConfigManager
from ....Storage import Storage
from ._response import DownloadResponse

@Resource.app.get("/api/{pool}/files/{id}/download/json")
async def download_json(pool: str, id: str):
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
        file_uuid = UUID(id)
    except ValueError:
        return ORJSONResponse(
            DownloadResponse(
                status = "error",
                message = "Invalid file id"
            ).model_dump(exclude_none=True),
            status_code=400
        )
    
    file_name = f"{file_uuid}{suffix}"
    
    if not storage.exists(file_name):
        return ORJSONResponse(
            DownloadResponse(
                status = "error",
                message = "File not found"
            ).model_dump(exclude_none=True),
            status_code=404
        )
    
    file = await storage.load(file_name)

    try:
        data = orjson.loads(file)
    except orjson.JSONDecodeError:
        logger.error(f"Failed to decode file {file_name}")
        return ORJSONResponse(
            DownloadResponse(
                status = "error",
                message = "Failed to decode file"
            ).model_dump(exclude_none=True),
            status_code=500
        )
    
    logger.info(
        "File loaded: {file_uuid}",
        module = "API/Download/JSON",
        file_uuid = file_uuid
    )

    return ORJSONResponse(
        DownloadResponse(
            status = "success",
            message = "File loaded",
            data = data
        ).model_dump(exclude_none=True),
        status_code=200
    )