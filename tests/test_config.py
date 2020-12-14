import os

import pytest

from magicbandreader.config import yaml_config


YAML_FILE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test_config.yaml')


def test_yaml_config():
    c = yaml_config(YAML_FILE, 'cmd')
    assert_test_yaml(c)


def test_yaml_config_FileNotFoundError():
    with pytest.raises(FileNotFoundError):
        yaml_config('bogus_file_name', 'cmd')


def test_yaml_config_TypeError():
    with pytest.raises(TypeError):
        yaml_config(None, 'cmd')


def test_yaml_config_cmd_None():
    c = yaml_config(YAML_FILE, None)
    assert_test_yaml(c)


def assert_test_yaml(c):
    assert c['test_1'] == 'test_value_1'
    assert c['test_2'] == 'test_value_2'
    assert c['test_3'] == 'test_value_3'
