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

# TODO: Fix 404s in content to avoid errors in wget
.PHONY: dist
dist:
	rm -rf $@
	-wget \
		--no-verbose \
		--directory-prefix $@ \
		--no-host-directories \
		--recursive \
		--max-redirect=0 \
		--adjust-extension \
		--retry-connrefused \
		http://localhost:$(PORT)

.PHONY: deploy
deploy:
	rsync -avz dist/ webfaction:$(webapp_dir)
