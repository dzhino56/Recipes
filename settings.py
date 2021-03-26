import yaml
from pathlib import Path


__all__ = ('load_config', )


def load_config():
    default_file = Path(__file__).parent / 'config.yaml'
    with open(default_file, 'r') as f:
        config = yaml.safe_load(f)

    return config
