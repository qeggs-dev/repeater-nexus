from fastapi.responses import ORJSONResponse
from loguru import logger
from uuid import UUID

from ..._resource import Resource
from ....Global_Config import GlobalConfigManager
from ....Storage import Storage

@Resource.app.delete("/api/{pool}/files/{id}/remove")
async def remove(pool: str, id: str):
    path = GlobalConfigManager.get_configs().storage.storage_path
    suffix = GlobalConfigManager.get_configs().storage.file_suffix
    try:
        storage = Storage(path, pool)
    except ValueError as e:
        return ORJSONResponse(
            {
                "status": "error",
                "message": str(e)
            },
            status_code=400
        )
    try:
        uuid = UUID(id)
    except ValueError:
        return ORJSONResponse(
            {
                "status": "error",
                "message": "Invalid file id"
            }, status_code=400
        )
    
    file_name = f"{uuid}{suffix}"

    storage.delete(file_name)
    logger.info(
        "File saved: {file_uuid}",
        module = "API/Upload/JSON",
        file_uuid = uuid
    )
        
    return ORJSONResponse(
        content = {
            "status": "success",
            "file_uuid": uuid
        }
    )