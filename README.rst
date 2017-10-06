jahhills.com
============

Reboot of `hallelujahthehills.com <http://hallelujahthehills.com>`_
using the `Django <https://www.djangoproject.com/>`_ web framework 
and the `Bourbon <http://bourbon.io/>`_ family of SASS libraries.

Launched on April 12, 2016, in conjunction with the band's fifth album,
`A Band Is Something To Figure Out <http://hallelujahthehills.com/music/a-band-is-something-to-figure-out/>`_.

As with the `first iteration <http://github.com/bhrutledge/hallelujahthehills.com>`_,
this is an exercise in using the framework. This time around, the focus is on
`test-driven development <http://www.obeythetestinggoat.com/>`_,
`best practices <http://twoscoopspress.org/collections/everything/products/two-scoops-of-django-1-8>`_,
and `YAGNI <http://en.wikipedia.org/wiki/You_aren't_gonna_need_it>`_.
Launched as a `MVP <https://en.wikipedia.org/wiki/Minimum_viable_product>`_,
with enhancements and bugs across the stack tracked in
`GitHub Issues <https://github.com/bhrutledge/jahhills.com/issues>`_.


Getting Started
---------------

Install `pip-tools <https://github.com/jazzband/pip-tools>`_
(e.g., with `pipsi <https://github.com/mitsuhiko/pipsi>`_).

Clone this repo.

Create and activate a Python 3.6 virtual environment.

Copy ``hth/hth/settings/env.example`` to ``.env`` in the same directory, then
edit to change settings.

Bootstrap and validate the environment with ``fab dev bootstrap``.

Start ``runserver`` with ``fab dev serve``.

Manage pacakges with ``pip-compile`` and ``pip-sync``.

Install Sass tools with ``bundle install``


Deployment
----------

Dump local content changes with ``fab dev dumpdata``.

Commit and push to GitHub.

Deploy with ``fab prod deploy``.
