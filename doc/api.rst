DskLayout API
*************

This is an official API documentation for the dsklayout_ python package.

.. _Introduction:

Introduction
============

The dsklayout_ package consists of several modules comprising a complete
foundation for the dsklayout_ application. The modules found in dsklayout_
package may be depicted in a layered fashion. The topmost module is then
:mod:`dsklayout.cli` which implements command-line interface. At the same
level there could be a module called ``dsklayout.gui`` implementing graphical
user interface, but it's not being developed at the moment. One level down,
there is a module called :mod:`dsklayout.cmd`, which implements commands
performed by dsklayout_ application (a complete, parametrized command
algorithms, configured and triggered through front-ends such as
:mod:`dsklayout.cli`).  Commands provided by :mod:`dsklayout.cmd` use
lower-level modules, such as :mod:`dsklayout.probe` (gathering information from
operating system), :mod:`dsklayout.device` (abstracting block devices), and
other modules providing some rudimentary stuff. The full index of modules
may be found in Modules_.


.. _Modules:

Modules
=======

This section documents python modules provided by the dsklayout_ package. The
summary below lists all the modules and provides links to full documentation.

.. autosummary::
    :toctree: api/modules

    dsklayout.archive
    dsklayout.cli
    dsklayout.cmd
    dsklayout.device
    dsklayout.graph
    dsklayout.probe
    dsklayout.util
    dsklayout.visitor

.. _dsklayout: https://github.com/ptomulik/dsklayout
