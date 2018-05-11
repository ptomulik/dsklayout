#!/usr/bin/env python3

import tempfile
import urllib.request as request
import subprocess
import sys
import argparse


parser = argparse.ArgumentParser(description="""
Install pip with get-pip.py.
See https://pip.pypa.io/en/latest/installing/#install-pip
""")

parser.add_argument('--url', dest='url', type=str,
                    default='https://bootstrap.pypa.io/get-pip.py',
                    help='url address of the get-pip.py')
parser.add_argument('--python', dest='python', type=str,
                    default=sys.executable,
                    help='python executable to be used as subprocess')


args, unknown = parser.parse_known_args(sys.argv[1:])

with request.urlopen(args.url) as req, \
     tempfile.NamedTemporaryFile(prefix='get-pip-', suffix='.py') as tmp:
    tmp.write(req.read())
    subprocess.run([args.python, tmp.name ] + unknown)
