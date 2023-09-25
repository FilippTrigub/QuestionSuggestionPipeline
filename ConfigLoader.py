import os

import yaml


class ConfigObject:
    def __init__(self, dictionary):
        for key, value in dictionary.items():
            if isinstance(value, dict):
                setattr(self, key, ConfigObject(value))
            else:
                setattr(self, key, value)


def merge_configs(default, custom):
    """Recursive function to merge custom config into default config."""
    for key, value in custom.items():
        if key in default and isinstance(default[key], dict):
            merge_configs(default[key], value)
        else:
            default[key] = value
    return default


def load_config(qs_config_path, main_config_path=None):
    # Load the default config from the subdirectory
    with open(qs_config_path, 'r') as file:
        default_config = yaml.safe_load(file)

    # Load the main config from the root directory (if it exists)
    if main_config_path and os.path.exists(main_config_path):
        with open(main_config_path, 'r') as file:
            main_config = yaml.safe_load(file)
            # Merge configurations
            merged_config = merge_configs(default_config, main_config)
    else:
        merged_config = default_config

    # Convert merged config to a ConfigObject
    return ConfigObject(merged_config)


def find_file_path(root_dir: str, target_file_name: str) -> str:
    """
    Searches for a specific file name in the root dir and all sub dir and returns the path from the root dir to the file.

    :param root_dir: The directory to start the search from.
    :param target_file_name: The name of the file to search for.
    :return: The path from root_dir to the file if found, else None.
    """
    for foldername, _, filenames in os.walk(root_dir):
        if target_file_name in filenames:
            return os.path.relpath(os.path.join(foldername, target_file_name), root_dir)
    return None


config = load_config(qs_config_path=find_file_path('.', 'default_config.yaml'),
                     main_config_path=find_file_path('.', 'src/config.yaml'))
