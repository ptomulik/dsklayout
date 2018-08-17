#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest
from unittest.mock import patch

import dsklayout.util.misc_ as misc_

class Test__Misc(unittest.TestCase):

    def test__add_dict_getters__01(self):
        class T:
            _mappings = {'foo_bar' : 'foo-bar', 'quux' : 'quux'}
            def __init__(self):
                self._dict = dict()

        misc_.add_dict_getters(T, T._mappings, '_dict')

        t = T()
        t._dict['foo-bar'] = 'ok'
        self.assertEqual(t.foo_bar, 'ok')
        self.assertIsNone(t.quux)
        with self.assertRaises(AttributeError):
            t.unmapped



if __name__ == '__main__':
    unittest.main()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
