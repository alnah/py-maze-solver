ENV=env
PIP=$(ENV)/bin/pip
RUFF=$(ENV)/bin/ruff
PYRIGHT=$(ENV)/bin/pyright
PYINSTALLER=$(ENV)/bin/pyinstaller
BUILDNAME=maze
TARGET=/usr/local/bin

.PHONY: default run env install-dev check test fmt lintfix lsp install clean

default: build clean

check: env lsp fmt test

env:
	$(info 🌍 ACTIVATING ENVIRONMENT...)
	@if [ ! -d "$(ENV)" ]; then python -m venv $(ENV); fi

install: env
	$(info 📥 DOWNLOADING DEPENDENCIES...)
	$(PIP) install -r requirements.txt
	

install-dev: env
	$(info 📥 DOWNLOADING DEPENDENCIES...)
	$(PIP) install -r requirements_dev.txt

lsp: env
	$(info 🛠️ CHECKING STATIC TYPES...)
	$(PYRIGHT)

lintfix: env
	$(info 🔍 RUNNING LINT TOOLS...)
	$(RUFF) check --select I --fix

fmt: env
	$(info ✨ CHECKING CODE FORMATTING...)
	$(RUFF) format

test: env
	$(info 🧪 TESTING...)
	python -m unittest discover -s .

run:
	$(info 🚀 RUNNING APP...)
	python3 main.py 

build: install
	$(info 🏗️ BUILDING THE PROJECT...)
	$(PYINSTALLER) --onefile --noconsole --name $(BUILDNAME) main.py
	mv dist/$(BUILDNAME) $(TARGET)

clean:
	$(info 🧹 CLEANING UP...)
	rm -rf build/ dist/
	rm $(BUILDNAME).spec
