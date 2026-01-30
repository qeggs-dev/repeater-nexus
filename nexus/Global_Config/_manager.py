from __future__ import annotations
from ._model import GlobalConfig
from typing import ClassVar

class GlobalConfigManager:
    _config: GlobalConfig = GlobalConfig()
    _instance: ClassVar[GlobalConfigManager] | None = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def update_config(cls, config: GlobalConfig):
        if not isinstance(config, GlobalConfig):
            raise TypeError("config must be an instance of GlobalConfig")
        cls._config = config
    
    @classmethod
    def get_configs(cls) -> GlobalConfig:
        return cls._config