import orjson

from fastapi.responses import ORJSONResponse
from loguru import logger
from uuid import uuid4

from ..._resource import Resource
from ....Global_Config import GlobalConfigManager
from ....Storage import Storage
from ._request import SubmitRequest

@Resource.app.post("/api/{pool}/submit")
async def submit_json(pool: str, request: SubmitRequest):
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
    while True:
        resource_uuid = uuid4()
        if not storage.resource_exists(resource_uuid):
            break
    
    for key, value in request.content.items():
        await storage.save(resource_uuid, key, value)
    
    return ORJSONResponse(
        {
            "status": "ok",
            "message": "submit success",
            "resource_uuid": str(resource_uuid)
        },
        status_code=200
    )