#!/usr/bin/env bash
# Production settings for www.hallelujahthehills.com on webfaction

# Assuming PATH and PORT is set by supervisord. For example:
# [program:jahhills]
# command=$APP_DIR/start.sh
# redirect_stderr=true
# environment=PATH=$APP_DIR/venv/bin:%(ENV_PATH)s,PORT=$APP_PORT

# Need `exec` for `supervisorctl stop` to work
exec gunicorn \
    --pythonpath "${BASH_SOURCE%/*}" \
    --env DJANGO_SETTINGS_MODULE=hth.settings \
    --bind 127.0.0.01:$PORT \
    --workers 4 \
    --access-logfile - \
    --error-logfile - \
    hth.wsgi:application
