# jahhills.com

Reboot of [hallelujahthehills.com](http://hallelujahthehills.com) using the [Django](https://www.djangoproject.com/) web framework and the [Bourbon](http://bourbon.io/) family of SASS libraries.

Launched on April 12, 2016, in conjunction with the band's fifth album, [A Band Is Something To Figure Out](http://hallelujahthehills.com/music/a-band-is-something-to-figure-out/).

As with the [first iteration](http://github.com/bhrutledge/hallelujahthehills.com), this is an exercise in using the framework. This time around, the focus is on [test-driven development](http://www.obeythetestinggoat.com/), [best practices](http://twoscoopspress.org/collections/everything/products/two-scoops-of-django-1-11), and [YAGNI](http://en.wikipedia.org/wiki/You_aren't_gonna_need_it). Launched as an [MVP](https://en.wikipedia.org/wiki/Minimum_viable_product), with enhancements and bugs across the stack tracked in [GitHub Issues](https://github.com/bhrutledge/jahhills.com/issues).

## Getting Started

Clone this repo.

Create and activate a Python 3.6 virtual environment.

Copy `hth/settings/env.example` to `.env` in the same directory, then edit to change settings.

Bootstrap and validate the environment with `make`.

Start `runserver` with `make serve`.

Manage packages with `pip-compile` and `pip-sync` from [pip-tools](https://github.com/jazzband/pip-tools).

## Compiling CSS

Install [Bundler](https://bundler.io).

Install Sass tools with `bundle install`.

Recompile CSS on Sass changes with `make css`.

## Production infrastructure

- Hosted on [Webfaction](https://www.webfaction.com)
- Managed by [Supervisor](http://supervisord.org/index.html)
- HTTPS via [Let's Encrypt](https://letsencrypt.org)
- Monitoring via [UptimeRobot](https://uptimerobot.com)

## Deployment

Dump local content changes with `make dumpdata`.

Commit and push to GitHub.

SSH to server.

Activate virtual environment.

Update environment with `DJANGO_SETTINGS_MODULE=hth.settings.prod make`

Restart process with `supervisorctl restart jahhills`.
