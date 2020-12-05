#!/usr/bin/env bash
# Production settings for www.hallelujahthehills.com on webfaction

# Assuming PORT is set by supervisord. For example:
# [program:jahhills]
# command=$APP_DIR/start.sh
# redirect_stderr=true
# environment=PORT=$APP_PORT

project_dir=${BASH_SOURCE%/*}

# Need `exec` for `supervisorctl stop` to work
exec "$project_dir/venv/bin/gunicorn" \
    --pythonpath "$project_dir" \
    --env DEBUG=False \
    --env DJANGO_SETTINGS_MODULE=hth.settings \
    --bind 127.0.0.01:"${PORT:=8000}" \
    --workers 4 \
    --access-logfile - \
    --error-logfile - \
    hth.wsgi:application
