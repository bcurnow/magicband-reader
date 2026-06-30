import sys
from glob import glob
from unittest.mock import MagicMock

# These modules either fail or are unavailable outside RPi hardware;
# inject mocks before any test module triggers the imports.
sys.modules['board'] = MagicMock()
sys.modules['neopixel'] = MagicMock()


def convert_to_module_name(string: str):
    return string.replace('/', '.').replace('\\', '.').replace('.py', '')


pytest_plugins = [
    convert_to_module_name(fixture) for fixture in glob('tests/fixtures/*.py') if '__' not in fixture
]
