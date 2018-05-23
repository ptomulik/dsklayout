.. _man-dsklayout-dot:

dsklayout dot
=============

SYNOPSIS
--------

**dsklayout dot [options] [DEV [DEV ...]]**

DESCRIPTION
-----------

Generate graph representing relations between the existing block devices,
partitions, and so forth. The resultant graph is expressed in `DOT language`_
defined by graphviz_.


OPTIONS
-------

.. program:: dsklayout


.. rubric:: Positional arguments


.. option:: DEV

    List of the top-level block devices (disks) to be included in backup. If
    the list is empty (missing), all detected block devices are included,
    except the ``-i`` option is given.


.. rubric:: Generic options


.. option:: -i, --input=INFILE

    Read the graph from INFILE. The INFILE should be an archive created with
    :ref:`man-dsklayout-backup`.


.. rubric:: Paths to external programs


.. option:: --lsblk=PROG

    Path to :manpage:`lsblk(8)` executable


.. rubric:: Other options


.. option:: --tmpdir-prefix=PFX

    Prefix for temporary directory name.


.. _DOT language: https://graphviz.org/doc/info/lang.html
.. _graphviz: https://graphviz.org/
