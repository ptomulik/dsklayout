DskLayout - Developer's Guidelines
==================================

Setting up development environment
----------------------------------

We recommend using pip_ + pipenv_ to manage dependencies and run programs in
an isolated Python environment.

Installing pip user-wise
````````````````````````

If you don't have pip_ installed, it may be installed as follows

.. code:: shell

    python3 install-pip.py --user

The ``install-pip.py`` script accepts all options of the `get-pip.py`_ script,
see `pip installation instructions`_. It also provides some additional options,
see ``python3 install-pip.py --help`` for its local options.


Installing pipenv user-wise
```````````````````````````

Provided pip_ is already installed, invoke

.. code:: shell

    python3 -m pip install pipenv --user

See also `pipenv docs`_.

Preparing virtual environment for development
`````````````````````````````````````````````

Installing packages (and creating virtualenv, if it doesn't exist)

.. code:: shell

    python3 -m pipenv install --dev

To remove the virtualenv later

.. code:: shell

    python3 -m pipenv --rm

Installing docker-compose
`````````````````````````

Follow `docker compose installation`_ instructions.

Performing developer's tasks
----------------------------

Running commands in pipenv isolated environment
````````````````````````````````````````````````

Example of running unit-tests

.. code:: shell

    python3 -m pipenv run ./runtests.sh

Generating documentation
````````````````````````

.. code:: shell

    python3 -m pipenv run make html

The generated documentation is written to ``build/doc/html``.


Analyzing code with codeclimate
```````````````````````````````

Provided `docker compose`_ is already installed

.. code:: shell

      docker-compose run codeclimate analyze


LICENSE
-------

Copyright (c) 2018 by Pawel Tomulik

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE

.. _pip: https://pypi.org/project/pip/
.. _pipenv: https://pipenv.org/
.. _pip installation instructions: https://pip.pypa.io/en/latest/installing/#install-pip
.. _get-pip.py: https://bootstrap.pypa.io/get-pip.py
.. _pipenv docs: https://docs.pipenv.org/
.. _docker compose installation: https://docs.docker.com/compose/install/
.. _docker compose: https://docs.docker.com/compose/
