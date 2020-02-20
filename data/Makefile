HOST ?= 127.0.0.1
PORT ?= 8001

name := hth-datasette
django_db := $(realpath $(CURDIR)/..)/hth/jahhills.sqlite3
data_sql := dump_apps.sql
data_db := hth.sqlite3
metadata := metadata.json

.PHONY: serve
serve: $(data_db)
	datasette --metadata $(metadata) --host $(HOST) --port $(PORT) $<

.PHONY: publish
publish: $(data_db)
	datasette publish heroku --name $(name) \
		--metadata $(metadata) \
		--install datasette-vega \
		--install datasette-cluster-map \
		--install datasette-render-html \
		$<

$(data_db): $(django_db) $(data_sql)
	rm -f $@
	sqlite3 $(django_db) <$(data_sql) | sqlite3 $@
