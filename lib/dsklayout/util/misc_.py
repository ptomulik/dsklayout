# -*- coding: utf8 -*-
"""Miscellaneous utilities
"""

__all__ = ('add_dict_getters',
           'select_items',
           'select_keys',
           'select_values',
           'select_values_attr')


def add_dict_getters(cls, mappings, dict):
    """Add property getters to a class. The properties are assumed to be kept
    in an internal dictionary."""
    for attr, key in mappings.items():
        setattr(cls, attr, property(lambda o, k=key: getattr(o, dict).get(k)))


def select_items(items, pred=lambda x: True, use_key=False):
    """Generate items satisfying given condition.

     If ``pred(v)`` (when ``use_key=False``) or ``pred(k, v)`` (when
     ``use_key=True``) is ``True`` for a given item ``(k,v)`` from **items**,
     then ``(k,v)`` will be included in the result, otherwise the item will be
     omitted.

    :param items:
        input sequence to be looked up,
    :param pred:
        a function in form ``pred(n)``, if **use_key** is ``False`` (default),
        or ``pred(k,n)`` if **use_key** is ``True``,
    :param bool use_key:
        if ``True``, then key is passed as the first argument to **pred**,
        and node value as second.
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

        list(select_items(items, lambda x: x.surname == 'Smith'))
        # [('js', Person('John', 'Smith')), ('ms', Person('Mary', 'Smith'))]
        list(select_items(items, lambda x: x.name == 'John'))
        # [('js', Person('John', 'Smith')), ('jb', Person('John', 'Brown'))]
    """
    if use_key:
        return ((k, n) for k, n in items.items() if pred(k, n))
    else:
        return ((k, n) for k, n in items.items() if pred(n))

def select_keys(items, pred=lambda x: True, use_key=False):
    """Generate node keys for items satisfying given condition.

     If ``pred(v)`` (when ``use_key=False``) or ``pred(k, v)`` (when
     ``use_key=True``) is ``True`` for a given item ``(k,v)`` from **items**,
     then ``k`` will be included in the result, otherwise the item will be
     omitted.

    :param items:
        input sequence to be looked up,
    :param pred:
        a function in form ``pred(n)``, if **use_key** is ``False`` (default),
        or ``pred(k,n)`` if **use_key** is ``True``,
    :param bool use_key:
        if ``True``, then key is passed as the first argument to **pred**,
        and node value as second.
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

        list(select_keys(items, lambda x: x.surname == 'Smith'))
        # ['js', 'ms']
        list(select_keys(items, lambda x: x.name == 'John'))
        # ['js', 'jb']
    """
    return (k for k, _ in select_items(items, pred, use_key))

def select_values(items, pred=lambda x: True, use_key=False):
    """Generate node values for items satisfying given condition.

     If ``pred(v)`` (when ``use_key=False``) or ``pred(k, v)`` (when
     ``use_key=True``) is ``True`` for a given item ``(k,v)`` from **items**,
     then ``v`` will be included in the result, otherwise the item will be
     omitted.

    :param items:
        input sequence to be looked up,
    :param pred:
        a function in form ``pred(n)``, if **use_key** is ``False`` (default),
        or ``pred(k,n)`` if **use_key** is ``True``,
    :param bool use_key:
        if ``True``, then key is passed as the first argument to **pred**,
        and node value as second.
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

        list(select_values(items, lambda x: x.surname == 'Smith'))
        # [Person('John', 'Smith'), Person('Marry', 'Smith')]
        list(select_values(items, lambda x: x.name == 'John'))
        # [Person('John', 'Smith'), Person('John', 'Brown')]
    """
    return (n for _, n in select_items(items, pred, use_key))

def select_values_attr(items, attr, pred=lambda x: True, use_key=False):
    """Generate attribute values for items satisfying given condition.

     If ``pred(v)`` (when ``use_key=False``) or ``pred(k, v)`` (when
     ``use_key=True``) is ``True`` for a given item ``(k,v)`` from **items**,
     then ``getattr(v, attr)`` will be included in the result, otherwise the
     item will be omitted.

    :param items:
        input sequence to be looked up,
    :param pred:
        a function in form ``pred(v)`` if **use_key** is ``False`` (default) or
        ``pred(k, v)`` if **use_key** is ``True``,
    :param bool use_key:
        if ``True``, then key is passed as the first argument to **pred**,
        and node value as second.
    :return:
        a generator object iterating over attribute values for selected items.

    :example:

    .. code:: python

        from dsklayout.util import select_values_attr

        class Person:
            def __init__(self, name, surname):
                self.name = name
                self.surname = surname

        items = {'js': Person('John', 'Smith'),
                 'jb': Person('John', 'Brown'),
                 'ms': Person('Mary', 'Smith')}

        list(select_values_attr(items, 'name', lambda x: x.surname == 'Smith'))
        # ['John', 'Marry']
        list(select_values_attr(items, 'surname', lambda x: x.name == 'John'))
        # ['Smith', 'Brown']
    """
    return (getattr(n, attr) for _, n in select_items(items, pred, use_key))


# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
