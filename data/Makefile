HOST ?= 127.0.0.1
DATA_PORT ?= 8002

name := hth-datasette
django_db := $(realpath $(CURDIR)/..)/hth/jahhills.sqlite3
dump_sql := dump_apps.sql
data_db := hth.sqlite3
metadata := metadata.yaml

.PHONY: serve
serve: $(data_db)
	datasette --cors --metadata $(metadata) --host $(HOST) --port $(DATA_PORT) $(data_db)

.PHONY: publish
publish: $(data_db)
	datasette publish fly --app $(name) \
		--metadata $(metadata) \
		--install datasette-vega \
		--install datasette-cluster-map \
		--install datasette-render-html \
		$(data_db)

$(data_db): $(django_db) $(dump_sql) $(view_sql)
	rm -f $(data_db)
	sqlite3 $(django_db) <$(dump_sql) | sqlite3 $(data_db)
