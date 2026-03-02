import orjson

from os import PathLike
from loguru import logger
from pathlib import Path

from .API import Resource
from .Global_Config import GlobalConfigManager, GlobalConfig
from .Logger_Init import logger_init
from ._info import __version__

class NexusCore:
    def init_logger(self):
        logger_init(GlobalConfigManager.get_configs().logger)
    
    def load_configs(self, path: str | PathLike = "./configs/global_config.json"):
        path = Path(path)
        try:
            with open(path, "rb") as f:
                GlobalConfigManager.update_config(
                    GlobalConfig(
                        **orjson.loads(
                            f.read()
                        )
                    )
                )
        except Exception as e:
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, "wb") as f:
                f.write(
                    orjson.dumps(
                        GlobalConfigManager.get_configs().model_dump()
                    )
                )
            logger.warning(f"Failed to load configs from {path}, created a new one. Error: {e}")
    
    def init_all_resources(self):
        Resource.init_all()
    
    def run(self):
        logger.info("Starting Nexus...")
        logger.info(
            "Version: {version}",
            version = __version__
        )
        Resource.run(
            host = GlobalConfigManager.get_configs().server.host,
            port = GlobalConfigManager.get_configs().server.port,
            reload = GlobalConfigManager.get_configs().server.reload,
            workers = GlobalConfigManager.get_configs().server.workers
        )