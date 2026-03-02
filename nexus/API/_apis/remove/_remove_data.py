from fastapi.responses import ORJSONResponse
from loguru import logger
from uuid import UUID

from ..._resource import Resource
from ....Global_Config import GlobalConfigManager
from ....Storage import Storage

@Resource.app.delete("/api/{pool}/resources/{resource_id}/remove/data/{data_id}")
async def remove_data(pool: str, resource_id: str, data_id: str):
    path = GlobalConfigManager.get_configs().storage.storage_path
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
        resource_uuid = UUID(resource_id)
    except ValueError:
        return ORJSONResponse(
            {
                "status": "error",
                "message": "Invalid file id"
            }, status_code=400
        )
    
    try:
        storage.remove_data(resource_uuid, data_id)
    except ValueError as e:
        return ORJSONResponse(
            {
                "status": "error",
                "message": str(e)
            },
            status_code=400
        )
        
    return ORJSONResponse(
        content = {
            "status": "success",
            "message": "File removed"
        }
    )