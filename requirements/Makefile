venv := $(realpath $(CURDIR)/..)/venv
bin := $(venv)/bin

ifeq ($(DEBUG), True)
env=dev
else
env=base
endif

.PHONY: all
all: $(venv)
	$(bin)/pip-compile $(args) base.in > /dev/null
	$(bin)/pip-compile $(args) dev.in > /dev/null

.PHONY: install
install: $(venv)
	$(bin)/pip-sync $(env).txt

.PHONY: check
check: $(venv)
	$(bin)/pip list --outdated
	$(bin)/safety check -r dev.txt

$(venv):
	python3 -m venv $@
	$(bin)/pip install --upgrade setuptools pip pip-tools

.PHONY: help
help:
	@echo "make            Recompile requirements after changing *.in"
	@echo "make args=-U    Recompile requirements to upgrade all dependencies"
	@echo "make check      Show outdated or vulnerable dependencies"
