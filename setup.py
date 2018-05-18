#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

about = {}
with open(os.path.join(here, 'lib', 'dsklayout', '__version__.py')) as f:
    exec(f.read(), about)

setup(name='dsklayout',
      version=about['__version__'],
      description='Retrieve and backup layouts of block devices (disks)',
      author='Paweł Tomulik',
      author_email='ptomulik@meil.pw.edu.pl',
      url='https://github.com/ptomulik/dsklayout',
      packages=find_packages('lib'),
      package_dir={'': 'lib'},
      license='MIT',
      install_requires=[
      ],
      extras_require={
        'dev': [
            'sphinx'
        ]
      },
      include_package_data=True,
      entry_points={
          'console_scripts':[
              'dsklayout=dsklayout.cli:main'
          ]
      }
)
