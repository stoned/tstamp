#!/bin/sh -
: ${PORT:=5000}
: ${HOST:=0.0.0.0}
exec /usr/bin/env FLASK_APP=tstamp.py flask run -h "$HOST" -p "$PORT" "$@"
