# Explorable database

Powered by [Datasette](https://datasette.readthedocs.io/en/stable/).

<http://hth-datasette.herokuapp.com/hth>

Some interesting queries:

- [Gigs per venue](http://hth-datasette.herokuapp.com/hth?sql=select%0D%0Av.name+as+venue%2C%0D%0Av.city%2C%0D%0Acount%28g.id%29+as+gigs%2C%0D%0Amin%28g.date%29+as+first_show%2C%0D%0Amax%28g.date%29+as+last_show%2C%0D%0Av.latitude%2C%0D%0Av.longitude%0D%0Afrom+shows_gig+as+g%0D%0Ajoin+shows_venue+as+v+on+g.venue_id+%3D+v.id%0D%0Awhere+v.longitude+%3C+-70%0D%0Agroup+by+v.id%0D%0Aorder+by+gigs+desc%2C+last_show+desc)
- [Gigs per year](http://hth-datasette.herokuapp.com/hth?sql=select%0D%0Astrftime%28%27%25Y%27%2C+date%29+as+year%2C%0D%0Acount%28id%29+as+gigs%0D%0Afrom+shows_gig%0D%0Agroup+by+year#g.mark=bar&g.x_column=year&g.x_type=ordinal&g.y_column=gigs&g.y_type=quantitative)
- [Release aggregates](http://hth-datasette.herokuapp.com/hth?sql=select%0D%0A++r.title%2C%0D%0A++strftime(%27%25Y%27%2C+r.date)+as+year%2C%0D%0A++count(distinct+s.id)+as+tracks%2C%0D%0A++count(distinct+v.id)+as+videos%2C%0D%0A++count(distinct+p.id)+as+press%0D%0Afrom%0D%0A++music_release+as+r%0D%0A++join+music_song+as+s+on+s.release_id+%3D+r.id%0D%0A++join+music_video+as+v+on+v.release_id+%3D+r.id%0D%0A++join+music_press+as+p+on+p.release_id+%3D+r.id%0D%0Agroup+by%0D%0A++r.id%0D%0Aorder+by%0D%0A++r.date+desc%0D%0A)

## Publishing the data

Install Datasette on your system, e.g. using [pipx](https://pipxproject.github.io/pipx/):

```
$ pipx install datasette
$ pipx inject datasette datasette-cluster-map datasette-vega datasette-render-html
```

In the root directory of this project, update the database:

```
$ make update
```

Explore locally at <http://127.0.0.1:8001>:

```
$ make -C data
```

Publish to Heroku:

```
$ make -C data publish
```
