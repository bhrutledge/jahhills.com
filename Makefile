HOST ?= 127.0.0.1
PORT ?= 8000
ENV ?= dev

bin := $(CURDIR)/venv/bin
python := $(bin)/python
manage := $(python) manage.py
fixture := hth/jahhills.json
apps := music news shows

.PHONY: all
all: update test loaddata

.PHONY: update
update:
	$(bin)/pip install -U setuptools pip pip-tools
	$(bin)/pip-sync requirements/$(ENV).txt
	$(manage) migrate --noinput
	$(manage) collectstatic --noinput

.PHONY: lint
lint:
	$(bin)/flake8 hth

.PHONY: test
test: lint
	$(bin)/pytest --cov --cov-report=html

.PHONY: dumpdata
dumpdata:
	$(manage) dumpdata --indent=4 $(apps) > $(fixture)

.PHONY: loaddata
loaddata:
	$(manage) loaddata $(fixture)

.PHONY: serve
serve:
	$(manage) runserver_plus $(HOST):$(PORT)

.PHONY: css
css:
	bundle exec sass --watch static/sass:static/css
