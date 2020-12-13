HOST ?= 127.0.0.1
PORT ?= 8000

bin := $(CURDIR)/venv/bin
python := $(bin)/python
manage := $(python) manage.py

fixture_apps := music news shows
fixture := hth/jahhills.json

keyfile := .localhost-key.pem
certfile := .localhost.pem
certnames := localhost $(HOST)

# This and `make deploy` have been replaced by `netlify deploy`
# Leaving them in as an example for rsync-based deployment
webhost := webfaction:webapps/jahhills_static

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

# Serving via https:// to ensure that Cloudinary URLS are https://
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

# See macOS gotcha: https://github.com/FiloSottile/mkcert/issues/199
$(keyfile):
	mkcert -key-file $(keyfile) -cert-file $(certfile) $(certnames)

# Inspired by https://apex.sh/blog/post/pre-render-wget/
# Using --max-redirect=0 to catch missing trailing slashes,
# which cause redirects, which yield spurious .html files
wget := wget --no-verbose \
		--directory-prefix=dist \
		--no-host-directories \
		--adjust-extension \
		--retry-connrefused \
		--max-redirect=0

server := https://$(HOST):$(PORT)

.PHONY: html
html: 404
	$(wget) --recursive --level=inf --execute robots=off $(server)

# Ignoring expected 404 error from wget, but letting others through
.PHONY: 404
404:
	error=`$(wget) --content-on-error $(server)/404 2>&1` ;\
	code=$$? ;\
	[[ $$error =~ "ERROR 404" ]] || ( echo $$error; exit $$code )

.PHONY: dist
dist:
	set -e ;\
	rm -rf dist ;\
	make update ;\
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
		dist/ $(webhost)
