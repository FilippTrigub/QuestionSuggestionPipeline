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


def load_config(qs_config_path, main_config_path):
    # Load the default config from the subdirectory
    with open(qs_config_path, 'r') as file:
        default_config = yaml.safe_load(file)

    # Load the main config from the root directory (if it exists)
    if os.path.exists(main_config_path):
        with open(main_config_path, 'r') as file:
            main_config = yaml.safe_load(file)
            # Merge configurations
            merged_config = merge_configs(default_config, main_config)
    else:
        merged_config = default_config

    # Convert merged config to a ConfigObject
    return ConfigObject(merged_config)


config = load_config(qs_config_path='src/QuestionSuggestionPipeline/default_config.yaml',
                     main_config_path='src/config.yaml')
