#!/bin/sh -
: ${PORT:=5000}
: ${HOST:=0.0.0.0}
export PORT
export HOST
exec python3 tstamp.py "$@"
