SCRIPT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
APP_NAME := Mac Apps Uninstaller
APP_VERSION := 1.0.0

default:
	echo "Running main.py with venv..."
	source "${SCRIPT_DIR}/.venv/bin/activate" && \
	python3 "${SCRIPT_DIR}/main.py"

install:
	python3 -m venv .venv
	source "${SCRIPT_DIR}/.venv/bin/activate" && \
	pip3 install -r "${SCRIPT_DIR}/requirements.txt"

upgrade:
	source "${SCRIPT_DIR}/.venv/bin/activate" && \
	pip3 install --upgrade pip

# Create the .icns icon file
icon:
	source "${SCRIPT_DIR}/.venv/bin/activate" && \
	python3 "${SCRIPT_DIR}/create_icns.py"

# Install build dependencies
build-deps:
	source "${SCRIPT_DIR}/.venv/bin/activate" && \
	pip3 install py2app

# Build the application with py2app
build: build-deps
	source "${SCRIPT_DIR}/.venv/bin/activate" && \
	python3 "${SCRIPT_DIR}/create_icns.py" && \
	cd "${SCRIPT_DIR}" && \
	CODESIGN_IDENTITY="-" python3 setup.py py2app --no-chdir || \
	(echo "Build completed but with code signing issues - attempting to fix..." && \
	codesign --force --deep --sign - "dist/Mac Apps Uninstaller.app" && \
	echo "Build completed successfully with ad-hoc signing") && \
	open "dist/Mac Apps Uninstaller.app"

# Build the application in development mode (faster, for testing)
dev-build: build-deps icon
	source "${SCRIPT_DIR}/.venv/bin/activate" && \
	python3 setup.py py2app -A

# Clean up build artifacts
clean:
	rm -rf build
	rm -rf dist
	rm -f app_icon.icns

# Clean everything including the virtual environment
clean-all: clean
	rm -rf .venv

# Help target
help:
	@echo "Available targets:"
	@echo "  default   - Run the application using Python"
	@echo "  install   - Create virtual environment and install dependencies"
	@echo "  upgrade   - Upgrade pip in the virtual environment"
	@echo "  icon      - Create the application icon (.icns file)"
	@echo "  build     - Build the standalone macOS application (.app)"
	@echo "  dev-build - Build the application in development mode (faster)"
	@echo "  clean     - Remove build artifacts"
	@echo "  clean-all - Remove build artifacts and virtual environment"
	@echo "  help      - Show this help message"