import aiofiles

from os import PathLike
from pathlib import Path
from typing import Generator
from loguru import logger

from ..Global_Config import GlobalConfigManager
from ..Assist import validate_path

class Storage:
    def __init__(self, base_path: str | PathLike, pool: str):
        self._base_path = Path(base_path)
        if not self.validate_file_name(pool):
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
    
    def validate_file_name(self, file: str | PathLike) -> bool:
        return validate_path(self._base_path, file)
    
    def get_file_path(self, file: str | PathLike) -> Path:
        return self.pool_path / file
    
    async def load(self, file: str | PathLike) -> bytes | None:
        if self.validate_file_name(file):
            file_path = self.get_file_path(file)
            async with aiofiles.open(file_path, mode = "rb") as f:
                data = await f.read()
            logger.info(
                "Loaded file {file}",
                file = file_path.name
            )
            return data
        else:
            return None
    
    async def save(self, file: str | PathLike, content: bytes) -> None:
        if self.validate_file_name(file):
            file_path = self.get_file_path(file)
            if not file_path.parent.exists():
                file_path.parent.mkdir(parents = True)
            async with aiofiles.open(file_path, mode = "wb") as f:
                await f.write(content)
            logger.info(
                "Saved file {file}",
                file = file_path.name
            )
        else:
            raise ValueError("Path is invalid")
    
    def delete(self, file: str | PathLike) -> None:
        if self.validate_file_name(file):
            file_path = self.get_file_path(file)
            if file_path.exists():
                file_path.unlink()
                logger.info(
                    "Deleted file {file}",
                    file = file_path.name
                )
        else:
            raise ValueError("Path is invalid")
    
    def exists(self, file: str | PathLike) -> bool:
        if self.validate_file_name(file):
            file_path = self.get_file_path(file)
            return file_path.exists()
        else:
            return False
    
    def files(self) -> Generator[str, None, None]:
        base_path = self.pool_path
        for file in base_path.iterdir():
            if file.is_file():
                yield file.name
    
    def filelist(self) -> list[str]:
        return list(self.files())