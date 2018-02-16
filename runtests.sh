#!/bin/sh

SCRIPTDIR="`dirname $0`"

(cd $SCRIPTDIR && PYTHONPATH=lib python3 -m unittest discover -p '*Tests.py')
