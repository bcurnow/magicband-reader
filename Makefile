IMAGE_NAME := $(notdir $(CURDIR))
VENV := .venv
PYTHON := $(VENV)/bin/python
SOUNDS_DIR := $(abspath $(CURDIR)/../sounds)

.PHONY: help build clean coverage docker-build docker-run format install lint release setup test

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "%-15s %s\n", $$1, $$2}'

setup: ## Create .venv and install all dependencies (run once; activate with: source .venv/bin/activate)
	python3 -m venv $(VENV)
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt

install: ## Install dependencies into the active environment (use 'setup' to also create the venv)
	pip install -r requirements.txt

test: ## Run the test suite
	pytest

coverage: ## Run the test suite and report coverage
	coverage run -m pytest
	coverage report

lint: ## Check code with ruff
	ruff check .

format: ## Format code with ruff
	ruff format .

build: ## Build the Python wheel
	python setup.py bdist_wheel

clean: ## Remove build artifacts and coverage data (pass CLEAN_VENV=1 to also remove .venv)
	rm -rf build dist *.egg-info .coverage .ruff_cache
	$(if $(CLEAN_VENV),rm -rf $(VENV))

release: ## Create a GitHub release. Usage: make release VERSION=1.0.3 (or pre-create a git tag first)
	@set -e; \
	if [ -n "$(VERSION)" ]; then \
		VER="$(VERSION)"; TAG="v$(VERSION)"; CREATE_TAG=1; \
	else \
		TAG=$$(git describe --tags --abbrev=0 2>/dev/null); \
		[ -n "$$TAG" ] || { echo "Error: VERSION required. Usage: make release VERSION=1.0.3"; exit 1; }; \
		VER=$${TAG#v}; CREATE_TAG=0; \
	fi; \
	sed -i "s/version=\"[^\"]*\"/version=\"$$VER\"/" setup.py; \
	git add setup.py; \
	git diff --cached --quiet || git commit -m "Release $$VER"; \
	[ "$$CREATE_TAG" = "0" ] || git rev-parse "$$TAG" >/dev/null 2>&1 || git tag -a "$$TAG" -m "Release $$VER"; \
	git push origin main; \
	git push origin "$$TAG"; \
	rm -rf build dist *.egg-info; \
	python setup.py sdist bdist_wheel; \
	gh release create "$$TAG" dist/* \
		--title "$$TAG" \
		--notes "$$(awk -v ver="$$VER" '/^# /{if($$0 == "# " ver){found=1; next} else if(found){exit}} found{print}' CHANGELOG.md)"

docker-build: ## Build the Docker image
	docker image build \
		--build-arg USER_ID=$(shell id -u) \
		--build-arg GROUP_ID=$(shell id -g) \
		-t $(IMAGE_NAME):latest \
		.

docker-run: ## Run a shell in the Docker container (mounts project root, /dev, and ../sounds)
	docker run -it \
		--privileged \
		--mount src="$(CURDIR)",target=/$(IMAGE_NAME),type=bind \
		--mount src=/dev,target=/dev,type=bind \
		--mount src="$(SOUNDS_DIR)",target=/sounds,type=bind \
		$(IMAGE_NAME):latest \
		/bin/bash
