HOST ?= 127.0.0.1
PORT ?= 8000

bin := $(CURDIR)/venv/bin
python := $(bin)/python
manage := $(python) manage.py
fixture := hth/jahhills.json
apps := music news shows
process := $(notdir $(CURDIR))
webapp := jahhills_staging
webapp_dir := webapps/$(webapp)
branch := $(shell git rev-parse --abbrev-ref HEAD)

.PHONY: update
update:
	make -C requirements install
	$(manage) check
	$(manage) migrate --noinput
	$(manage) loaddata $(fixture)
	$(manage) collectstatic --noinput

.PHONY: dumpdata
dumpdata:
	$(manage) dumpdata --indent=4 $(apps) > $(fixture)

.PHONY: test
test: lint
	$(bin)/pytest --cov --cov-report=html --cov-report=term

.PHONY: lint
lint:
	$(bin)/flake8 hth

.PHONY: serve
serve:
	$(manage) runserver_plus $(HOST):$(PORT)

.PHONY: css
css:
	bundle exec sass --watch hth/static/sass:hth/static/css

.PHONY: docs
docs:
	make -C docs html

.PHONY: restart
restart:
	supervisorctl restart $(process)
	supervisorctl status $(process)

.PHONY: deploy
deploy:
	ssh webfaction 'bash -l -c "\
		cd $(webapp_dir) && \
		git checkout $(branch) && \
		git pull && \
		make update restart"'
