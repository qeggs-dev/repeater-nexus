import orjson

from fastapi.responses import ORJSONResponse
from loguru import logger
from uuid import uuid4

from ..._resource import Resource
from ....Global_Config import GlobalConfigManager
from ....Storage import Storage
from ._request import SubmitRequest

@Resource.app.post("/api/{pool}/submit/json")
async def submit_json(pool: str, request: SubmitRequest):
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
    while True:
        file_uuid = uuid4()
        file_name = f"{file_uuid}{suffix}"
        if not storage.exists(file_name):
            break
    
    data = orjson.dumps(request.content)
    await storage.save(file_name, data)
    logger.info(
        "File saved: {file_uuid}",
        module = "API/Upload/JSON",
        file_uuid = file_uuid
    )

    if request.timeout is not None:
        async def delete_file():
            storage.delete(file_name)
            logger.info(
                "File deleted: {file_uuid}",
                module = "API/Upload/JSON",
                file_uuid = file_uuid
            )
        
        await Resource.delayed_tasks_pool.add_task(
            sleep_time = request.timeout,
            task = delete_file()
        )
        
    return ORJSONResponse(
        content = {
            "status": "success",
            "file_uuid": file_uuid
        }
    )