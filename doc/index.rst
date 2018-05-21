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

DskLayout is a small tool for a backup of partition tables, filesystem
metadata, raid metadata, logical volumes, etc.. We don't backup files stored on
filesystems, a lot of great tools already exists for this purpose. What we do,
is to backup all the information necessary to quickly recreate empty
filesystems on spare disks in a disaster recovery scenario.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
