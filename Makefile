
default:
	echo "Running main.py with venv..."
	source "${PWD}/.venv/bin/activate"
	python3 main.py

install:
	python3 -m venv .venv
	source "${PWD}/.venv/bin/activate"
	pip3 install -r requirements.txt

upgrade:
	source "${PWD}/.venv/bin/activate"
	pip3 install --upgrade pip