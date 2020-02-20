HOST ?= 127.0.0.1
PORT ?= 8001

name := hth-datasette
django_db := $(realpath $(CURDIR)/..)/hth/jahhills.sqlite3
django_apps := music news shows
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

$(data_db): $(django_db)
	rm -f $@
	@for app in $(django_apps); do \
		sql=".dump $${app}_%" ; \
		echo $$sql ; \
		sqlite3 $< "$$sql" | sqlite3 $@ ; \
	done
