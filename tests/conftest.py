from glob import glob


def convert_to_module_name(string: str):
    return string.replace('/', '.').replace('\\', '.').replace('.py', '')


pytest_plugins = [
    convert_to_module_name(fixture) for fixture in glob('tests/fixtures/*.py') if '__' not in fixture
]
