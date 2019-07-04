.PHONY: all
all:
	pip-compile prod.in > /dev/null
	pip-compile dev.in > /dev/null

.PHONY: upgrade
upgrade:
	pip-compile -U prod.in > /dev/null
	pip-compile -U dev.in > /dev/null

.PHONY: safety
safety:
	safety check -r dev.txt

.PHONY: help
help:
	@echo "make            Recompile requirements after changing *.in"
	@echo "make upgrade    Recompile requirements to upgrade all dependencies"
