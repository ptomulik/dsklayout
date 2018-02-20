#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest
import unittest.mock as mock

import dsklayout.action.action_ as action_


class TestAction(action_.Action):
    def __init__(self, method):
        self._method = method
    @property
    def method(self):
        return self._method

class Test__Action(unittest.TestCase):

    def test__is_abstract(self):
        with self.assertRaises(TypeError) as context:
            action_.Action()
        self.assertIn('abstract', str(context.exception))

    def test__call__(self):
        subject = mock.Mock(spec=['foo'])
        subject.foo = mock.Mock(return_value='ok')
        action = TestAction('foo')
        self.assertEqual(action(subject), 'ok')
        subject.foo.assert_called_once_with(action)



if __name__ == '__main__':
    unittest.main()

# vim: set ft=python et ts=4 sw=4:
