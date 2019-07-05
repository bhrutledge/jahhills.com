bin := $(realpath $(CURDIR)/../venv/bin)

ifeq ($(DEBUG), True)
env=dev
else
env=base
endif

.PHONY: all
all: tools
	$(bin)/pip-compile $(args) base.in > /dev/null
	$(bin)/pip-compile $(args) dev.in > /dev/null

.PHONY: install
install: tools
	$(bin)/pip-sync $(env).txt

.PHONY: tools
tools:
	$(bin)/pip install -U setuptools pip pip-tools

.PHONY: safety
safety:
	$(bin)/safety check -r dev.txt

.PHONY: help
help:
	@echo "make            Recompile requirements after changing *.in"
	@echo "make args=-U    Recompile requirements to upgrade all dependencies"
	@echo "make safety     Check requirements for security vulnerabilities"
