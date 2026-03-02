import orjson
import shutil
import asyncio
import aiofiles

from os import PathLike
from pathlib import Path
from typing import Generator
from loguru import logger
from uuid import UUID
from typing import Any, NoReturn

from ._fname_b64_encoder import fname_b64_encode, fname_b64_decode
from ..Global_Config import GlobalConfigManager
from ..Assist import validate_path

class Storage:
    def __init__(self, base_path: str | PathLike, pool: str):
        self._base_path = Path(base_path)
        if not validate_path(self._base_path, pool):
            raise ValueError("Invalid pool name")
        pool_white_list = GlobalConfigManager.get_configs().storage.pool_whitelist
        if pool not in pool_white_list:
            raise ValueError("Pool name not in whitelist")
        self._pool = pool
    
    @property
    def base_path(self):
        return self._base_path
    
    @property
    def pool(self):
        return self._pool
    
    @property
    def pool_path(self) -> Path:
        return self.base_path / self.pool
    
    def validate_data(self, resource_id: UUID, data_id: str) -> bool:
        return validate_path(self._base_path, self.get_data_path(resource_id, data_id))
    
    def validate_resource(self, resource_id: UUID) -> bool:
        return validate_path(self._base_path, self.get_resource_path(resource_id))
    
    def raise_check_resource(self, resource_id: UUID) -> None | NoReturn:
        if not self.validate_resource(resource_id):
            raise ValueError(f"Resource {resource_id} is invalid")
    
    def raise_check_data(self, resource_id: UUID, data_id: str) -> None | NoReturn:
        if not self.validate_data(resource_id, data_id):
            raise ValueError(f"Data {data_id}/{resource_id} is invalid")
    
    def get_resource_path(self, resource_id: UUID) -> Path:
        return self.pool_path / str(resource_id)
    
    def get_data_path(self, resource_id: UUID, data_id: str) -> Path:
        return self.get_resource_path(resource_id) / (fname_b64_encode(data_id) + GlobalConfigManager.get_configs().storage.file_suffix)
    
    async def load(self, resource_id: UUID, data_id: str) -> Any | None:
        self.raise_check_data(resource_id, data_id)
        file_path = self.get_data_path(resource_id, data_id)
        async with aiofiles.open(file_path, mode = "rb") as f:
            data = orjson.loads(await f.read())
        logger.info(
            "Loaded {resource_id}/{data_id}",
            resource_id = str(resource_id),
            data_id = data_id
        )
        return data
    
    async def save(self, resource_id: UUID, data_id: str, content: Any) -> None:
        self.raise_check_data(resource_id, data_id)
        file_path = self.get_data_path(resource_id, data_id)
        if not file_path.parent.exists():
            file_path.parent.mkdir(parents = True)
        async with aiofiles.open(file_path, mode = "wb") as f:
            await f.write(orjson.dumps(content))
        logger.info(
            "Saved {resource_id}/{data_id}",
            resource_id = str(resource_id),
            data_id = data_id
        )
    
    def remove_data(self, resource_id: UUID, data_id: str) -> None:
        self.raise_check_data(resource_id, data_id)
        file_path = self.get_data_path(resource_id, data_id)
        if file_path.exists():
            file_path.unlink()
            logger.info(
                "Deleted {resource_id}/{data_id}",
                resource_id = str(resource_id),
                data_id = data_id
            )
    
    def remove_resource(self, resource_id: UUID) -> None:
        self.raise_check_resource(resource_id)
        file_path = self.get_resource_path(resource_id)
        if file_path.exists():
            asyncio.to_thread(
                shutil.rmtree,
                file_path
            )
            logger.info(
                "Deleted {resource_id}",
                resource_id = str(resource_id)
            )

    def resource_exists(self, resource_id: UUID) -> bool:
        self.raise_check_resource(resource_id)
        file_path = self.get_resource_path(resource_id)
        return file_path.exists()
    
    def data_exists(self, resource_id: UUID, data_id: str) -> bool:
        self.raise_check_data(resource_id, data_id)
        file_path = self.get_data_path(resource_id, data_id)
        return file_path.exists()
    
    def resources(self) -> Generator[str, None, None]:
        base_path = self.pool_path
        for file in base_path.iterdir():
            if file.is_file():
                yield file.name
    
    def datas(self, resource_id: UUID) -> Generator[str, None, None]:
        self.raise_check_resource(resource_id)
        base_path = self.get_resource_path(resource_id)
        for file in base_path.iterdir():
            yield fname_b64_decode(file.stem)
    
    def filelist(self) -> list[str]:
        return list(self.resources())