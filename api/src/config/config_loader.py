import os
import tomllib
base_dir = os.path.dirname(os.path.abspath(__file__))

configs = {}

def load_config(config_file: str = "settings.toml"):
    global configs
    config_path = os.path.join(base_dir, config_file)
    if not configs:
        with open(config_path, "rb") as file:
            config = tomllib.load(file)
        
        for section, values in config.items():
            for key, value in values.items():
                if not value:
                    config[section][key] = os.environ.get(key, "")
        configs = config
    return configs
