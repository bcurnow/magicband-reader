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
    python_requires='>=3.7',
    dependency_links=['http://github.com/bcurnow/repo/tarball/master#egg=rfidreader[evdev, mfrc522]'],
    install_requires=[
        'Click',
        'click-config-file',
        'adafruit-circuitpython-neopixel',
        'rpi-ws281x',
        'pydub',
        'simpleaudio',
        'pyyaml',
        'rfidreader >= 2.0.1',
    ],
    entry_points={
        'console_scripts': [
            'magicband-reader=magicbandreader.reader:main',
        ],
    },
)
