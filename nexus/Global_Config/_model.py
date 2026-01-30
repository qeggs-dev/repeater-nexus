from pydantic import BaseModel, Field
from ._models import *

class GlobalConfig(BaseModel):
    server: ServerConfig = Field(default_factory=ServerConfig)
    logger: LoggerConfig = Field(default_factory=LoggerConfig)
    storage: StorageConfig = Field(default_factory=StorageConfig)