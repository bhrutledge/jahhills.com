# Explorable database

<https://data.hallelujahthehills.com/>

Powered by [Datasette](https://datasette.readthedocs.io/en/stable/).

## Publishing the data

[Install Datasette](https://docs.datasette.io/en/stable/installation.html) on your system, e.g. using Homebrew:

```sh
brew install datasette
datasette install datasette-cluster-map datasette-vega datasette-render-html datasette-publish-fly
```

In the root directory of this project, update the database:

```sh
make update
```

Explore locally at <http://127.0.0.1:8002>:

```sh
make -C data
```

[Install the Fly.io CLI](https://fly.io/docs/flyctl/install/):

```sh
brew install flyctl

flyctl auth login
```

Publish to Fly.io:

```sh
make -C data publish
```
