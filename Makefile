SCRIPT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

default:
	echo "Running main.py with venv..."
	source "${SCRIPT_DIR}/.venv/bin/activate"
	python3 "${SCRIPT_DIR}/main.py"

install:
	python3 -m venv .venv
	source "${SCRIPT_DIR}/.venv/bin/activate"
	pip3 install -r "${SCRIPT_DIR}/requirements.txt"

upgrade:
	source "${SCRIPT_DIR}/.venv/bin/activate"
	pip3 install --upgrade pip