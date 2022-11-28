HOST ?= 127.0.0.1
PORT ?= 8001

name := hth-datasette
django_db := $(realpath $(CURDIR)/..)/hth/jahhills.sqlite3
dump_sql := dump_apps.sql
view_sql := create_views.sql
data_db := hth.sqlite3
metadata := metadata.json

.PHONY: serve
serve: $(data_db)
	datasette --metadata $(metadata) --host $(HOST) --port $(PORT) $(data_db)

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
	sqlite3 $(data_db) <$(view_sql)
