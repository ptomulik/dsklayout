#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest
import dsklayout.probe.probe_ as probe_

class Test__Probe(unittest.TestCase):

    def test__content__1(self):
        content = ['item1', 'item2']
        probe = probe_.Probe(content)
        self.assertIs(probe.content, content)

    def test__dump_attributes(self):
        probe = probe_.Probe(['item1', 'item2'])
        self.assertEqual(probe.dump_attributes(), {'content': ['item1', 'item2']})

    def test__load_attributes(self):
        class X(probe_.Probe): pass
        probe = X.load_attributes({'content': ['item1', 'item2']})
        self.assertIsInstance(probe, X)
        self.assertEqual(probe.content, ['item1', 'item2'])


if __name__ == '__main__':
    unittest.main()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
