#!/usr/bin/env bash
# Production settings for www.hallelujahthehills.com on webfaction

# Assuming PATH is set by supervisor
# Need `exec` for `supervisorctl stop` to work
exec gunicorn \
    --pythonpath "${BASH_SOURCE%/*}" \
    --env DJANGO_SETTINGS_MODULE=hth.settings.prod \
    --bind 127.0.0.01:13149 \
    --workers 4 \
    --access-logfile - \
    --error-logfile - \
    hth.wsgi:application
