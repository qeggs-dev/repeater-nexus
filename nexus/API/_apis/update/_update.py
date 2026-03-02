import orjson

from fastapi.responses import ORJSONResponse
from loguru import logger
from uuid import UUID

from ..._resource import Resource
from ....Global_Config import GlobalConfigManager
from ....Storage import Storage
from ._request import UpdateRequest

@Resource.app.put("/api/{pool}/resources/{resource_id}/update")
async def update(pool: str, resource_id: str, request: UpdateRequest):
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
                "message": "Invalid Resource ID"
            },
            status_code=400
        )

    if not storage.resource_exists(resource_uuid):
        return ORJSONResponse(
            {
                "status": "error",
                "message": "Data not found"
            },
            status_code=404
        )
    
    for key, value in request.content.items():
        await storage.save(resource_uuid, key, value)
    
    return ORJSONResponse(
        {
            "status": "success",
            "message": "Data updated"
        },
        status_code=200
    )