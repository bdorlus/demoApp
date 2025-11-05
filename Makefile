.PHONY: setup install build run test

PYTHON ?= python3
VENV ?= .venv
VENV_PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

setup:
	$(PYTHON) -m venv --system-site-packages $(VENV)

install: setup requirements.txt
	@if grep -q '^[^#[:space:]]' requirements.txt; then \
		$(PIP) install --no-deps -r requirements.txt; \
	else \
		echo "No dependencies to install."; \
	fi

build: install

run: install
	$(VENV_PYTHON) -m uvicorn app.main:app --reload

test: install
	$(VENV_PYTHON) -m pytest --maxfail=1 --disable-warnings -q
