#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest
import unittest.mock as mock
from unittest.mock import patch

import dsklayout.probe.composite_ as composite_
import dsklayout.probe.probe_ as probe_

def here(member=None):
    if member is None:
        return 'test.dsklayout.probe.compositeTests'
    else:
        return 'test.dsklayout.probe.compositeTests.%s' % member

def there(member=None):
    if member is None:
        return 'dsklayout.probe.composite_'
    else:
        return 'dsklayout.probe.composite_.%s' % member


class Test__CompositeProbe(unittest.TestCase):

    def test__subclass_of_Probe(self):
        self.assertTrue(issubclass(composite_.CompositeProbe, probe_.Probe))

    def test__is_abstract(self):
        with self.assertRaises(TypeError) as context:
            composite_.CompositeProbe({})
        self.assertIn('abstract', str(context.exception))

    def test__subclassing(self):
        class T(composite_.CompositeProbe):
            @classmethod
            def probes(cls, **kw):
                return []
        self.assertIsInstance(T({}), composite_.CompositeProbe)

    def test__probes__1(self):
        self.assertIsNone(composite_.CompositeProbe.probes())

    def test__probes__2(self):
        self.assertIsNone(composite_.CompositeProbe.probes(foo='FOO',bar='BAR'))

    def test__available__1(self):
        A = mock.Mock()
        A.available = mock.Mock(return_value=True)
        B = mock.Mock()
        B.available = mock.Mock(return_value=True)
        with patch(there('CompositeProbe.probes'), return_value=[A, B]) as probes:
            self.assertTrue(composite_.CompositeProbe.available(foo='FOO'))
        A.available.assert_called_once_with(foo='FOO')
        B.available.assert_called_once_with(foo='FOO')

    def test__available__2(self):
        A = mock.Mock()
        A.available = mock.Mock(return_value=False)
        B = mock.Mock()
        B.available = mock.Mock(return_value=True)
        with patch(there('CompositeProbe.probes'), return_value=[A, B]) as probes:
            self.assertFalse(composite_.CompositeProbe.available(foo='FOO'))
        A.available.assert_called_once_with(foo='FOO')
        # B.available not called because A.available returned False

    def test__available__3(self):
        A = mock.Mock()
        A.available = mock.Mock(return_value=True)
        B = mock.Mock()
        B.available = mock.Mock(return_value=False)
        with patch(there('CompositeProbe.probes'), return_value=[A, B]) as probes:
            self.assertFalse(composite_.CompositeProbe.available(foo='FOO'))
        A.available.assert_called_once_with(foo='FOO')
        B.available.assert_called_once_with(foo='FOO')

    def test__mk_probes(self):
        A = mock.Mock()
        B = mock.Mock()
        C = mock.Mock()
        class T(composite_.CompositeProbe):
            @classmethod
            def probes(cls, **kw):
                return cls.mk_probes([A, B], {'c': C}, **kw)

        self.assertEqual(T.probes(), [A, B, C])
        self.assertEqual(T.probes(c=C()), [A, B])

    def test__extract_lsblk_graph__1(self):
        lsblk = mock.Mock()
        lsblk.graph = mock.Mock(return_value='graph')
        a = []
        f = []
        k = dict()

        with patch('dsklayout.probe.lsblk_.LsBlkProbe.new', return_value=lsblk) as new:
            self.assertEqual(composite_.CompositeProbe.extract_lsblk_graph(a, f, k), 'graph')
            new.assert_called_once_with(a, f, **k)
            lsblk.graph.assert_called_once_with()

    def test__extract_lsblk_graph__2(self):
        lsblk = mock.Mock()
        lsblk.graph = mock.Mock(return_value='graph1')

        a = ['a']
        f = ['f']
        k = {'foo': 'Foo'}

        with patch('dsklayout.probe.lsblk_.LsBlkProbe.new', return_value=lsblk) as new:
            self.assertEqual(composite_.CompositeProbe.extract_lsblk_graph(a, f, k), 'graph1')
            new.assert_called_once_with(a, f, **k)
            lsblk.graph.assert_called_once_with()

    def test__extract_lsblk_graph__3(self):
        lsblk = mock.Mock()
        lsblk.graph = mock.Mock(return_value='graph1')

        a = []
        f = []
        k = {'lsblkgraph': 'graph2'}

        with patch('dsklayout.probe.lsblk_.LsBlkProbe.new', return_value=lsblk) as new:
            self.assertEqual(composite_.CompositeProbe.extract_lsblk_graph(a, f, k), 'graph2')
            new.assert_not_called()
            lsblk.graph.assert_not_called()



if __name__ == '__main__':
    unittest.main()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
