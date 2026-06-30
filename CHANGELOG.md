# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]
### Fixed
- Replaced two `logging.warn` call sites with `logging.warning`; `logging.warn` was
  removed in Python 3.13 and crashed the process on the `python:3.13-slim` image.
- Fixed a malformed log message in `AbstractHandler.handle_event` that passed a
  2-tuple to the logger instead of a string.
- Fixed a race between `LightMickeyHandler` and `TurnOffMickeyHandler`: the LED
  fade-on thread is now tracked on the shared context and joined before
  `fade_off()` runs, instead of both writing to LED brightness concurrently.
- `reader.py` no longer drops falsy-but-valid RFID IDs (e.g. `0`, `""`); the read
  loop now checks `is not None` instead of truthiness.
- `LedController._brightness` now honors an explicit `brightness=0.0` instead of
  silently falling back to the instance default.
### Changed
- Modernized the project for Python 3.13: updated the Docker base image to
  `python:3.13-slim`, replaced `scripts/build.sh`/`scripts/docker.sh` with a
  Makefile, replaced flake8 with ruff, and fixed dependency/test issues
  surfaced by the upgrade.
