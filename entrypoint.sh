#!/bin/sh

. ./.venv/bin/activate
exec gunicorn config.wsgi:application -w 4 -b 0.0.0.0:$PORT --reload