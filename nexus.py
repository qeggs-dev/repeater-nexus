from nexus import NexusCore
from environs import Env

def main():
    env = Env()
    env.read_env()
    nexus = NexusCore()
    nexus.load_configs(env.str("CONFIG_PATH"))
    nexus.init_logger()
    nexus.init_all_resources()
    nexus.run()

if __name__ == "__main__":
    main()