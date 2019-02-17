outputs := prod.txt dev.txt

.PHONY: all
all: $(outputs)

.PHONY: clean
clean:
	rm $(outputs)

ifdef upgrade
ifeq ($(upgrade), all)
args += --upgrade
else
args += --upgrade-package $(upgrade)
endif
# Force recompilation, even though the input file hasn't changed
.PHONY: *.in
endif

$(outputs): %.txt: %.in
	@# Using --rebuild to avoid cache mismatches between dev environments
	pip-compile $(args) --rebuild --output-file $@ $< > /dev/null

# Assuming `-r prod.txt` in dev.in
dev.txt: prod.txt

.PHONY: safety
safety:
	safety check -r dev.txt

.PHONY: help
help:
	@echo "make                   Recompile requirements after changing *.in"
	@echo "make upgrade=all       Recompile requirements to upgrade all dependencies"
	@echo "make upgrade=Django    Recompile requirements to upgrade a single package"
