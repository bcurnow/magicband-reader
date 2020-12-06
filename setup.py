from setuptools import find_packages, setup


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='magicbandreader',
    version='1.0.0',
    author='Brian Curnow',
    author_email='brian.curnow+magicbandreader@gmail.com',
    description='Reads Disney MagicBands via the rfid-reader library and integrates with rfid-security-svc for implementing authorizations.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/bcurnow/magicband-reader',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: Apache Software License'
        'Operating System :: OS Independent',
        'Natural Language :: English',
    ],
    python_requires='>=3.9',
    install_requires=[
        'Click',
        'rfidreader@https://github.com/bcurnow/rfid-reader/releases/download/1.0.1/rfidreader-1.0.1-py3-none-any.whl',
        'Pygame',
        'RPi.GPIO',
        'adafruit-circuitpython-neopixel',
        'rpi-ws281x',
    ],
    entry_points={
        'console_scripts': [
            'magicband-reader=magicbandreader.reader:main',
        ],
    },
)
