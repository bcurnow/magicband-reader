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
* `--api-ssl-verify` - If True or a valid file reference, performs SSL validation, if false, skips validation (this is insecure!). Default: `CA.pem`
* `--authorized-sound` - The name of the sound file played when a band is authorized. Default: `authorized.wav`
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
