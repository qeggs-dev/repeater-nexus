from pydantic import BaseModel, Field

class StorageConfig(BaseModel):
    storage_path: str = "./workspace/storage"
    file_suffix: str = ".json"
    pool_whitelist: list[str] = Field(default_factory=list)