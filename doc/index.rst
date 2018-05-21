.. dsklayout documentation master file, created by
   sphinx-quickstart on Sun May 20 19:46:41 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

DskLayout: disk layout backups
******************************

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   api

Purpose
=======

DskLayout_ is a small tool used to back up partition tables, file-system
metadata, raid metadata, logical volumes, etc; namely all things we refer
here as "disk layout". We don't backup file-system contents (files), a lot of
great tools already exists for this purpose. What we do, is to backup all the
information necessary to quickly recreate empty file-systems on spare disks.

Requirements
============

#. **Python 3**: at minimum, python_ >= 3.4 is required.

#. **Command-line utilities**: DskLayout_ relies on several command-line
   utilities, such as :manpage:`lsblk(8)`, :manpage:`fdisk(8)`, provided by the
   following packages

   * Linux Debian

     .. code-block:: shell

        apt-get install util-linux fdisk gdisk lvm2

Installation
============

Via PyPi_

.. code-block:: shell

    python3 -m pip install dsklayout

Usage
=====

DskLayout_ provides single command-line program named ``dsklayout`` for all the
operations.

.. code-block:: shell

    dsklayout --help

The utility has several subcommands.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _DskLayout: https://github.com/ptomulik/dsklayout
.. _PyPi: https://pypi.org
.. _python: https://python.org
