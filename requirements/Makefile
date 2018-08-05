outputs := prod.txt dev.txt

.PHONY: all
all: $(outputs)

.PHONY: clean
clean:
	rm $(outputs)

ifdef upgrade
args += --upgrade-package $(upgrade)
# Force recompilation, even though the input file hasn't changed
.PHONY: *.in
endif

$(outputs): %.txt: %.in
	@# Using --rebuild to avoid cache mismatches between dev environments
	pip-compile $(args) --rebuild --output-file $@ $< > /dev/null

# Assuming `-r prod.txt` in dev.in
dev.txt: prod.txt

.PHONY: help
help:
	@echo "make                   Recompile requirements after changing *.in"
	@echo "make upgrade=Django    Recompile requirements to upgrade a single package"
