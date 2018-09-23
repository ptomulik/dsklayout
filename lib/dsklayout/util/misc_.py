# -*- coding: utf8 -*-
"""Miscellaneous utilities
"""

import re

__all__ = ('add_dict_getters',
           'select_items',
           'select_keys',
           'select_values',
           'select_attr',
           'snake_case')


def add_dict_getters(cls, mappings, dict):
    """Add property getters to a class. The properties are assumed to be kept
    in an internal dictionary."""
    for attr, key in mappings.items():
        setattr(cls, attr, property(lambda o, k=key: getattr(o, dict).get(k)))


def select_items(items, pred):
    """Select items satisfying given condition.

     If ``pred(x)`` returns true for a given item ``x`` from ``items.items()``,
     then ``x`` will be included in the result, otherwise ``x`` will be
     omitted.

    :param items:
        input sequence to be looked up,
    :param pred:
        a function in form ``pred(x)`` returning a boolean value,
    :return:
        a generator object iterating over values for selected items.

    :example:

    .. code:: python

        from dsklayout.util import select_items

        class Person:
            def __init__(self, name, surname):
                self.name = name
                self.surname = surname
            def __repr__(self):
                return 'Person(%s, %s)' % (self.name, self.surname)

        items = {'js': Person('John', 'Smith'),
                 'jb': Person('John', 'Brown'),
                 'ms': Person('Mary', 'Smith')}

        list(select_items(items, lambda x: x[1].surname == 'Smith'))
        # [('js', Person('John', 'Smith')), ('ms', Person('Mary', 'Smith'))]
        list(select_items(items, lambda x: x[1].name == 'John'))
        # [('js', Person('John', 'Smith')), ('jb', Person('John', 'Brown'))]
    """
    return (x for x in items.items() if pred(x))


def select_keys(items, pred):
    """Select item keys for items satisfying given condition.

     If ``pred(x)`` is ``True`` for a given item ``x`` from ``items.items()``,
     then ``x[0]`` (a key) will be included in the result, otherwise ``x``
     will be omitted.

    :param items:
        input sequence to be looked up,
    :param pred:
        a function in form ``pred(x)`` returning boolean value,
    :return:
        a generator object iterating over values for selected items.

    :example:

    .. code:: python

        from dsklayout.util import select_keys

        class Person:
            def __init__(self, name, surname):
                self.name = name
                self.surname = surname
            def __repr__(self):
                return 'Person(%s, %s)' % (self.name, self.surname)

        items = {'js': Person('John', 'Smith'),
                 'jb': Person('John', 'Brown'),
                 'ms': Person('Mary', 'Smith')}

        list(select_keys(items, lambda x: x[1].surname == 'Smith'))
        # ['js', 'ms']
        list(select_keys(items, lambda x: x[1].name == 'John'))
        # ['js', 'jb']
    """
    return (x[0] for x in select_items(items, pred))


def select_values(items, pred):
    """Select item values for items satisfying given condition.

     If ``pred(x)`` is ``True`` for a given item ``x`` from ``items.items()``,
     then ``x[1]`` (a value) will be included in the result, otherwise ``x``
     will be omitted.

    :param items:
        input sequence to be looked up,
    :param pred:
        a function in form ``pred(x)`` returning boolean value,
    :return:
        a generator object iterating over values for selected items.

    :example:

    .. code:: python

        from dsklayout.util import select_values

        class Person:
            def __init__(self, name, surname):
                self.name = name
                self.surname = surname
            def __repr__(self):
                return 'Person(%s, %s)' % (self.name, self.surname)

        items = {'js': Person('John', 'Smith'),
                 'jb': Person('John', 'Brown'),
                 'ms': Person('Mary', 'Smith')}

        list(select_values(items, lambda x: x[1].surname == 'Smith'))
        # [Person('John', 'Smith'), Person('Marry', 'Smith')]
        list(select_values(items, lambda x: x[1].name == 'John'))
        # [Person('John', 'Smith'), Person('John', 'Brown')]
    """
    return (n for _, n in select_items(items, pred))


def select_attr(items, attr, pred):
    """Select attribute values for items satisfying given condition.

     If ``pred(x)`` is ``True`` for a given item ``x`` from ``items.items()``,
     then ``getattr(x[1], attr)`` will be included in the result, otherwise
     ``x`` will be omitted.

    :param items:
        input sequence to be looked up,
    :param pred:
        a function in form ``pred(x)`` returning boolean value,
    :return:
        a generator object iterating over attribute values for selected items.

    :example:

    .. code:: python

        from dsklayout.util import select_attr

        class Person:
            def __init__(self, name, surname):
                self.name = name
                self.surname = surname

        items = {'js': Person('John', 'Smith'),
                 'jb': Person('John', 'Brown'),
                 'ms': Person('Mary', 'Smith')}

        list(select_attr(items, 'name', lambda x: x[1].surname == 'Smith'))
        # ['John', 'Marry']
        list(select_attr(items, 'surname', lambda x: x[1].name == 'John'))
        # ['Smith', 'Brown']
    """
    return (getattr(x[1], attr) for x in select_items(items, pred))


def snake_case(string):
    """Convert string to snake_case name.

    :param str string:
        a string to be converted.
    :return:
        **string** converted to snake case.
    :rtype: str
    """
    string = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', string)
    string = re.sub(r'(?:\s|-)+', '_', string)
    return string.lower()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
