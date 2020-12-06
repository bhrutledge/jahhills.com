HOST ?= 127.0.0.1
PORT ?= 8000

bin := $(CURDIR)/venv/bin
python := $(bin)/python
manage := $(python) manage.py

fixture_apps := music news shows
fixture := hth/jahhills.json

webhost := webfaction
webapp := jahhills_static
webapp_dir := webapps/$(webapp)

keyfile := .localhost-key.pem
certfile := .localhost.pem
certnames := localhost $(HOST)

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

.PHONY: serve-wsgi
serve-wsgi: $(keyfile) $(certfile)
	$(bin)/gunicorn \
		--env DEBUG=False \
		--env DJANGO_SETTINGS_MODULE=hth.settings \
		--bind $(HOST):$(PORT) \
		--keyfile $(keyfile) \
		--certfile $(certfile) \
		--workers 4 \
		--access-logfile - \
		--error-logfile - \
		hth.wsgi:application

$(keyfile):
	mkcert -key-file $(keyfile) -cert-file $(certfile) $(certnames)

# Using --max-redirect=0 to catch missing trailing slashes,
# which cause redirects, which yield spurious .html files
.PHONY: static
html:
	rm -rf dist
	wget --no-verbose \
		--directory-prefix=dist \
		--no-host-directories \
		--recursive \
		--level=inf \
		--adjust-extension \
		--max-redirect=0 \
		--retry-connrefused \
		--execute robots=off \
		https://$(HOST):$(PORT)

.PHONY: dist
dist:
	set -e ;\
	make serve-wsgi & make html ;\
	kill % ; wait

.PHONY: serve-dist
serve-dist:
	$(python) -m http.server \
		--directory dist \
		--bind $(HOST) $(PORT)

.PHONY: deploy
deploy:
	rsync --archive --compress --verbose \
		dist/ $(webhost):$(webapp_dir)
