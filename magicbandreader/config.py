""" Implements a YAML-base config file for click-config-file."""
import os

import yaml

def yaml_config(file_path, cmd_name):
    with open(os.path.abspath(file_path)) as file:
        return yaml.full_load(file)
