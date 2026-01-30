import orjson

from fastapi.responses import ORJSONResponse
from loguru import logger
from uuid import UUID

from ..._resource import Resource
from ....Global_Config import GlobalConfigManager
from ....Storage import Storage
from ._request import UpdateRequest

@Resource.app.get("/api/{pool}/files/{id}/update/json")
async def update_json(pool: str, id: str, request: UpdateRequest):
    path = GlobalConfigManager.get_configs().storage.storage_path
    suffix = GlobalConfigManager.get_configs().storage.file_suffix
    storage = Storage(path, pool)
    try:
        file_uuid = UUID(id)
    except ValueError:
        return ORJSONResponse(
            {
                "status": "error",
                "message": "Invalid file id"
            },
            status_code=400
        )
    
    file_name = f"{file_uuid}{suffix}"

    if not storage.exists(file_name):
        return ORJSONResponse(
            {
                "status": "error",
                "message": "File not found"
            },
            status_code=404
        )
    try:
        data = orjson.dumps(request.content)
    except orjson.JSONDecodeError:
        logger.error(f"Failed to decode file {file_name}")
        return ORJSONResponse(
            {
                "status": "error",
                "message": "Failed to decode file"
            },
            status_code=500
        )
    
    await storage.save(file_name, data)
    
    logger.info(
        "File loaded: {file_uuid}",
        module = "API/Download/JSON",
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
        {
            "status": "success",
            "message": "File uploaded"
        },
        status_code=200
    )