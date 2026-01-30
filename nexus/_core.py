import orjson

from os import PathLike
from .API import Resource
from .Global_Config import GlobalConfigManager, GlobalConfig
from .Logger_Init import logger_init

class NexusCore:
    def __init__(self):
        self.resource = Resource()
    
    def init_logger(self):
        logger_init(self.config.get_configs().logger_config)
    
    def load_configs(self, path: str | PathLike = "./configs/global_config.json"):
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
            with open(path, "wb") as f:
                f.write(
                    orjson.dumps(
                        self.config.get_configs().model_dump()
                    )
                )
    
    def run(self):
        self.resource.run(
            host = GlobalConfigManager.get_configs().server.host,
            port = GlobalConfigManager.get_configs().server.port,
            reload = GlobalConfigManager.get_configs().server.reload,
            workers = GlobalConfigManager.get_configs().server.workers
        )