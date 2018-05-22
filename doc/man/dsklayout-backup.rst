dsklayout backup
================

SYNOPSIS
--------


**dsklayout backup [options] OUTFILE [DEV [DEV ...]]**

DESCRIPTION
-----------

Backup layout of host's block devices. The subcommand probes operating system
using several command-line utilities such as :manpage:`lsblk(8)`,
:manpage:`fdisk(8)`, :manpage:`gdisk(8)`, :manpage:`vgcfgbackup(8)` to gather
information about block devices, partitions, raid matrices, logical volumes,
file-systems and their dependencies. The collected information is written to
``OUTFILE`` in a predefined format (ZIP archive) suitable for later recovery.


OPTIONS
-------

.. program:: dsklayout


.. rubric:: Positional arguments


.. option:: OUTFILE

    Name of the output file (archive) created by the command.

.. option:: DEV

    List of the top-level block devices (disks) to be included in backup. If
    the list is empty (missing), all detected block devices are included.


.. rubric:: Paths to external programs


.. option:: --lsblk=PROG

    Name or path to ``lsblk`` program

.. option:: --fdisk=PROG

    Name or path to ``fdisk`` program

.. option:: --sfdisk=PROG

    Name or path to ``sfdisk`` program

.. option:: --sgdisk=PROG

    Name or path to ``sgdisk`` program

.. option:: --vgcfgbackup=PROG

    Name or path to ``vgcfgbackup`` program


.. rubric:: Other options


.. option:: --tmpdir=DIR

    Where to create temporary directory.

.. option:: --tmpdir-prefix=PFX

    prefix for temporary directory name.
