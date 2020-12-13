# jahhills.com

Reboot of [hallelujahthehills.com](http://hallelujahthehills.com) using the [Django](https://www.djangoproject.com/) web framework and the [Bourbon](http://bourbon.io/) family of SASS libraries.

Launched on April 12, 2016, in conjunction with the band's fifth album, [A Band Is Something To Figure Out](http://hallelujahthehills.com/music/a-band-is-something-to-figure-out/).

As with the [first iteration](http://github.com/bhrutledge/hallelujahthehills.com), this is an exercise in using the framework. This time around, the focus is on [test-driven development](http://www.obeythetestinggoat.com/), [best practices](http://twoscoopspress.org/collections/everything/products/two-scoops-of-django-1-11), and [YAGNI](http://en.wikipedia.org/wiki/You_aren't_gonna_need_it). Launched as an [MVP](https://en.wikipedia.org/wiki/Minimum_viable_product), with enhancements and bugs across the stack tracked in [GitHub Issues](https://github.com/bhrutledge/jahhills.com/issues).

Deployed as a [static site](https://github.com/bhrutledge/jahhills.com/pull/142) to minimize server requirements.

Anyone is welcome to [explore the data](./data/README.md).

## Getting Started

Clone this repo.

Copy `hth/.env.example` to `hth/.env`, then edit to set values.

Set environment variable `DEBUG=True`, e.g. using [direnv](https://direnv.net/).

Bootstrap the environment with `make`.

Run the test suite with `make test`.

Start `runserver` with `make serve`.

## Compiling CSS

Install [Bundler](https://bundler.io).

Install Sass tools with `bundle install`.

Recompile CSS on Sass changes with `make css`.

## Production infrastructure

- Domain registered on [Namecheap](https://www.namecheap.com/) (w/ DNS and email forwarding)
- Static site hosted on [Netlify](https://www.netlify.com/)
- Media hosted on [Cloudinary](https://cloudinary.com/)
- Monitored with [UptimeRobot](https://uptimerobot.com)

## Deployment

Run the test suite with `make test`.

Dump local content changes with `make dumpdata`.

Commit and push to GitHub.

Build the static site with `make dist`.

View the static site with `netlify dev`.

Deploy and publish the static site with `netlify deploy`.

Publish the data with `make -C data publish`.
