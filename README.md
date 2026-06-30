# magicband-reader
Reads Disney MagicBands via the rfid-reader library and integrates with rfid-security-svc for implementing authorizations. This is inspired by the [MagicBand reader from Foolish Mortal Builders](https://www.youtube.com/watch?v=HJ8CTLgmcSk&t=503s).

# Running
This package installs a entry point named `magicband-reader`

# Configuration
## Command Line Arguments
The `magicband-reader` entry point accepts the following command line arguments:
* `-b`|`--brightness-level` - The brightness level of the LEDs. Range of 0.0 to 1.0 inclusive. Default: `.5`
* `-c`|`--config` - Specifies the YAML configuration file to read the configuration from.
* `-i`|`--inner-pixel-count` - The number of pixels that make up the inner ring. Default: `15`
* `-k`|`--api-key` - The API key to authenticate to rfid-security-svc.
* `-l`|`--log-level` - The logging level. Must be one of: debug, info, warning, error, critical. Default: `warning`
* `-o`|`--outer-pixel-count` - The number of pixels that make up the outer ring. Default: `40`
* `-p`|`--permission` - The name of the permission to validate before authorizing. Default: `Open Door`
* `-s`|`--sound-dir` - The directory containing the sound files. Default: `/sounds`
* `-t`|`--reader-type` - The type of RFID reader implementation to use. Default: `mfrc522`
* `-u`|`--api-url` - The rfid-security-svc base URL. Default: `https://ubuntu-devpi.local:5000/api/v1.0/`
* `-v`|`--volume-level` - The volume sounds should be played at. Range of 0.0 to 1.0 inclusive. Default: `.1`
* `--api-ssl-verify` - If True or a valid file reference, performs SSL validation, if false, skips validation (this is insecure!). Default: `ca.pem`
* `--authorized-sound` - The name of the sound file played when a band is authorized. Default: `authorized.wav`
* `--port-number` - The port number to listen for uid requests on. Default: `8080`
* `--read-sound` - The name of the sound file played when a band is read. Default: `read.wav`
* `--unauthorized-sound` - The name of the sound file played when a band is authorized. Default: `unauthorized.wav`

In addition to arguments for the MagicBand Reader itself, you can also pass arguments to the RFID Reader implementation. This is done by adding additional arguments in the format `<reader type>-<option name>`. For example, to pass the parameter `device_name` to the `evdev` implementation, simply add `evdev-device_name <device_name>` to the end of the command line.

## Environment Variables
All configuration options, with the exception of the RFID Reader implementation options, can be specified as environment variables. The variables names are prefixed with `MR_`. The remaining name is the same as the long argument name in uppercase with all dashes replaced with underscore. For example, to specify `--volume-level` as an environment variable, you'd set `MR_VOLUME_LEVEL`.

## Configuration File
One of the command line options is a configuration file. This allows all configuration options, with the exception of the RFID Reader implementation options, to be specified in a YAML configuration file. For example:

```
api_url: https://ubuntu-devpi.local:5000/api/v1.0/
api_key: your API key here
api_ssl_verify: CA.pem
log_level: warning
volume_level: .1
sound_dir: /sounds
authorized_sound: be-our-guest-be-our-guest-put-our-service-to-the-test.wav
unauthorized_sound: is-my-hair-out.wav
brightness_level: .5
outer_pixel_count: 40
inner_pixel_count: 15
```

Much like the environment variables, the long name is used, leading dashes are removed and all other dashes become underscores

# Development

## Makefile

A `Makefile` is provided with targets for common development tasks:

```
make setup        Create .venv and install all dependencies
make install      Install dependencies into the active environment
make test         Run the test suite
make coverage     Run tests and report coverage
make lint         Check code with ruff
make format       Format code with ruff
make build        Build the Python wheel
make clean        Remove build artifacts (CLEAN_VENV=1 also removes .venv)
make release      Create a GitHub release (VERSION=x.y.z)
make docker-build Build the Docker image
make docker-run   Run a shell in the Docker container
```

Run `make help` to see this list at any time.

## Local Python Environment

On Linux, ensure the following system packages are installed before running `make setup`:

```bash
sudo apt-get install build-essential python3-dev
```

Use the `setup` target to create a virtual environment and install all dependencies:

```bash
make setup
source .venv/bin/activate
```

After activating, use `make test`, `make lint`, etc. directly — they resolve to the venv Python automatically.

## Docker Environment

Docker is the preferred environment when testing against real hardware, as it handles device access and mounts the sounds directory automatically.

Build the image:

```bash
make docker-build
```

Run a shell inside the container (mounts the project root, `/dev`, and `../sounds`):

```bash
make docker-run
```

Inside the container, run tests or start an interactive session with full hardware access. The container runs as a non-root user matching your host's user and group IDs.
