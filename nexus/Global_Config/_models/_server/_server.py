from pydantic import BaseModel

class ServerConfig(BaseModel):
    """Server Model"""
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = False
    workers: int | None = None