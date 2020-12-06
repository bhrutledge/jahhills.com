HOST ?= 127.0.0.1
PORT ?= 8000

bin := $(CURDIR)/venv/bin
python := $(bin)/python
manage := $(python) manage.py

fixture_apps := music news shows
fixture := hth/jahhills.json

webapp := jahhills_static
webapp_dir := webapps/$(webapp)

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

.PHONY: start
start:
	./start.sh

# TODO: Add missing trailing slashes to content that cause redirects
# Without --max-redirect, this can yield spurious .html files
# With --max-redirect, wget exits with an error that can be ignored
.PHONY: dist
dist:
	rm -rf $@
	-wget \
		--no-verbose \
		--directory-prefix=$@ \
		--no-host-directories \
		--recursive \
		--level=inf \
		--adjust-extension \
		--max-redirect=0 \
		--retry-connrefused \
		--execute robots=off \
		http://localhost:$(PORT)

.PHONY: deploy
deploy:
	rsync -avz dist/ webfaction:$(webapp_dir)
