HOST ?= 127.0.0.1
PORT ?= 8000

bin := $(CURDIR)/venv/bin
python := $(bin)/python
manage := $(python) manage.py

fixture_apps := music news shows
fixture := hth/jahhills.json

webapp := jahhills_staging
webapp_dir := webapps/$(webapp)
webapp_branch := $(shell git rev-parse --abbrev-ref HEAD)
webapp_process := $(notdir $(CURDIR))

.PHONY: update
update:
	make -C requirements install
	$(manage) check
	$(manage) migrate --noinput
	$(manage) loaddata $(fixture)
	$(manage) collectstatic --noinput

.PHONY: dumpdata
dumpdata:
	$(manage) dumpdata --indent=4 $(fixture_apps) > $(fixture)

.PHONY: test
test: lint
	$(bin)/pytest --cov --cov-report=html --cov-report=term

.PHONY: lint
lint:
	$(bin)/flake8 hth

.PHONY: serve
serve:
	$(manage) runserver $(HOST):$(PORT)

.PHONY: css
css:
	bundle exec sass --watch hth/static/sass:hth/static/css

.PHONY: docs
docs:
	make -C docs html

.PHONY: deploy
deploy:
	ssh webfaction 'bash -l -c "\
		cd $(webapp_dir) && \
		git fetch && \
		git checkout $(webapp_branch) && \
		git merge --ff-only && \
		make update restart"'

.PHONY: restart
restart:
	supervisorctl restart $(webapp_process)
	supervisorctl status $(webapp_process)

django_db := hth/jahhills.sqlite3
data_dir := data
data_db := $(data_dir)/hth.sqlite3

.PHONY: datasette
datasette: $(data_db)
	datasette $(data_db)

$(data_db): $(django_db)
	rm -f $@
	mkdir -p $(data_dir)
	@for app in $(fixture_apps); do \
		sql=".dump $${app}_%" ; \
		echo $$sql ; \
		sqlite3 $< "$$sql" | sqlite3 $@ ; \
	done
