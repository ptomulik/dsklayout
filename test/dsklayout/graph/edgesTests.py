#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest

import dsklayout.graph.edges_ as edges_

class Test__Edges(unittest.TestCase):

    def test__init__0(self):
        edges = edges_.Edges()
        self.assertEqual(edges.data, dict())
        self.assertEqual(edges.successors_dict, dict())
        self.assertEqual(edges.predecessors_dict, dict())

    def test__init__1(self):
        edges = edges_.Edges([('s1', 't1'), ('s2', 't2')])
        self.assertEqual(edges.data, {('s1','t1'): None, ('s2','t2'): None})
        self.assertEqual(edges.successors_dict, {'s1': set(('t1',)), 's2': set(('t2',))})
        self.assertEqual(edges.predecessors_dict, {'t1': set(('s1',)), 't2': set(('s2',))})

    def test__init__2(self):
        edges = edges_.Edges([('s1', 't1'), ('s2', 't2'), ('s1', 't1')])
        self.assertEqual(edges.data, {('s1','t1'): None, ('s2','t2'): None})
        self.assertEqual(edges.successors_dict, {'s1': set(('t1',)), 's2': set(('t2',))})
        self.assertEqual(edges.predecessors_dict, {'t1': set(('s1',)), 't2': set(('s2',))})

    def test__init__3(self):
        edges = edges_.Edges([(('r1','s1'), 't1'), (('r2', 's2'), 't2')])
        self.assertEqual(edges.data, {(('r1','s1'),'t1'): None, (('r2','s2'), 't2'): None})
        self.assertEqual(edges.successors_dict, {('r1','s1'): set(('t1',)), ('r2', 's2'): set(('t2',))})
        self.assertEqual(edges.predecessors_dict, {'t1': set((('r1','s1'),)), 't2': set((('r2','s2'),))})

    def test__init__3_data_true(self):
        edges = edges_.Edges([(('s1','t1'), 'E1'), (('s2', 't2'), 'E2')], data=True)
        self.assertEqual(edges.data, {('s1','t1'): 'E1', ('s2','t2'): 'E2'})
        self.assertEqual(edges.successors_dict, {'s1': set(('t1',)), 's2': set(('t2',))})
        self.assertEqual(edges.predecessors_dict, {'t1': set(('s1',)), 't2': set(('s2',))})

    def test__init__3_edgedata_true(self):
        edges = edges_.Edges([(('s1','t1'), 'E1'), (('s2', 't2'), 'E2')], edgedata=True)
        self.assertEqual(edges.data, {('s1','t1'): 'E1', ('s2','t2'): 'E2'})
        self.assertEqual(edges.successors_dict, {'s1': set(('t1',)), 's2': set(('t2',))})
        self.assertEqual(edges.predecessors_dict, {'t1': set(('s1',)), 't2': set(('s2',))})

    def test__init__3_edgedata_true_data_false(self):
        edges = edges_.Edges([(('s1','t1'), 'E1'), (('s2', 't2'), 'E2')], edgedata=True, data=False)
        self.assertEqual(edges.data, {('s1','t1'): 'E1', ('s2','t2'): 'E2'})
        self.assertEqual(edges.successors_dict, {'s1': set(('t1',)), 's2': set(('t2',))})
        self.assertEqual(edges.predecessors_dict, {'t1': set(('s1',)), 't2': set(('s2',))})

    def test__init__4(self):
        edges = edges_.Edges({('s1','t1'): 'E1', ('s2','t2'): 'E2'})
        self.assertEqual(edges.data, {('s1','t1'): 'E1', ('s2','t2'): 'E2'})
        self.assertEqual(edges.successors_dict, {'s1': set(('t1',)), 's2': set(('t2',))})
        self.assertEqual(edges.predecessors_dict, {'t1': set(('s1',)), 't2': set(('s2',))})

    def test__init__4_data_false(self):
        edges = edges_.Edges({('r1','s1'): 't1', ('r2', 's2'): 't2'}, data=False)
        self.assertEqual(edges.data, {(('r1','s1'),'t1'): None, (('r2','s2'), 't2'): None})
        self.assertEqual(edges.successors_dict, {('r1','s1'): set(('t1',)), ('r2', 's2'): set(('t2',))})
        self.assertEqual(edges.predecessors_dict, {'t1': set((('r1','s1'),)), 't2': set((('r2','s2'),))})

    def test__init__4_edgedata_false(self):
        edges = edges_.Edges({('r1','s1'): 't1', ('r2', 's2'): 't2'}, edgedata=False)
        self.assertEqual(edges.data, {(('r1','s1'),'t1'): None, (('r2','s2'), 't2'): None})
        self.assertEqual(edges.successors_dict, {('r1','s1'): set(('t1',)), ('r2', 's2'): set(('t2',))})
        self.assertEqual(edges.predecessors_dict, {'t1': set((('r1','s1'),)), 't2': set((('r2','s2'),))})

    def test__init__4_edgedata_false_data_true(self):
        edges = edges_.Edges({('r1','s1'): 't1', ('r2', 's2'): 't2'}, edgedata=False, data=True)
        self.assertEqual(edges.data, {(('r1','s1'),'t1'): None, (('r2','s2'), 't2'): None})
        self.assertEqual(edges.successors_dict, {('r1','s1'): set(('t1',)), ('r2', 's2'): set(('t2',))})
        self.assertEqual(edges.predecessors_dict, {'t1': set((('r1','s1'),)), 't2': set((('r2','s2'),))})

    def test__init__5(self):
        edges = edges_.Edges({'s1': 'E1', 's2': 'E2'})
        self.assertEqual(edges.data, {('s','1'): 'E1', ('s','2'): 'E2'})
        self.assertEqual(edges.successors_dict, {'s': set(('1','2'))})
        self.assertEqual(edges.predecessors_dict, {'1': set(('s',)), '2': set(('s',))})

    def test__init__5_data_false(self):
        edges = edges_.Edges({'s1': 't1', 's2': 't2'}, data=False)
        self.assertEqual(edges.data, {('s1','t1'): None, ('s2','t2'): None})
        self.assertEqual(edges.successors_dict, {'s1': set(('t1',)), 's2': set(('t2',))})
        self.assertEqual(edges.predecessors_dict, {'t1': set(('s1',)), 't2': set(('s2',))})

    def test__init__6(self):
        edges = edges_.Edges(['pq', 'rs']) # yes, quite strange, so just warn you here...
        self.assertEqual(edges.data, {('p','q'): None, ('r','s'): None})

    def test__has_successors(self):
        edges = edges_.Edges([('p', 'q'), ('q', 'r'), ('q', 's')])
        self.assertTrue(edges.has_successors('p'))
        self.assertTrue(edges.has_successors('q'))
        self.assertFalse(edges.has_successors('r'))
        self.assertFalse(edges.has_successors('s'))
        self.assertFalse(edges.has_successors('x'))

    def test__has_predecessors(self):
        edges = edges_.Edges([('p', 'q'), ('q', 'r'), ('s', 'r')])
        self.assertFalse(edges.has_predecessors('p'))
        self.assertTrue(edges.has_predecessors('q'))
        self.assertTrue(edges.has_predecessors('r'))
        self.assertFalse(edges.has_predecessors('s'))
        self.assertFalse(edges.has_predecessors('x'))

    def test__has_neighbors(self):
        edges = edges_.Edges([('p', 'q'), ('q', 'r'), ('s', 'r')])
        self.assertTrue(edges.has_neighbors('p'))
        self.assertTrue(edges.has_neighbors('q'))
        self.assertTrue(edges.has_neighbors('r'))
        self.assertTrue(edges.has_neighbors('s'))
        self.assertFalse(edges.has_neighbors('x'))

    def test__successors__1(self):
        edges = edges_.Edges([('p', 'q')])
        self.assertEqual(type(edges.successors('p')), set)

    def test__successors__2(self):
        edges = edges_.Edges([('p', 'q'), ('q', 'r'), ('q', 's')])
        self.assertEqual(edges.successors('p'), set(('q',)))
        self.assertEqual(edges.successors('q'), set(('r','s')))
        self.assertEqual(edges.successors('r'), set())

    def test__successors__KeyError(self):
        edges = edges_.Edges([('p', 'q')])
        with self.assertRaises(KeyError) as context:
            edges.successors('n0')
        self.assertEqual(repr('n0'), str(context.exception))

    def test__predecessors__1(self):
        edges = edges_.Edges([('p', 'q')])
        self.assertEqual(type(edges.predecessors('q')), set)

    def test__predecessors__2(self):
        edges = edges_.Edges([('p', 'q'), ('q', 'r'), ('s', 'r')])
        self.assertEqual(edges.predecessors('p'), set())
        self.assertEqual(edges.predecessors('q'), set(('p',)))
        self.assertEqual(edges.predecessors('r'), set(('q','s')))
        self.assertEqual(edges.predecessors('s'), set())

    def test__predecessors__KeyError(self):
        edges = edges_.Edges([('p', 'q')])
        with self.assertRaises(KeyError) as context:
            edges.predecessors('n0')
        self.assertEqual(repr('n0'), str(context.exception))

    def test__neighbors__1(self):
        edges = edges_.Edges([('p', 'q')])
        self.assertEqual(type(edges.neighbors('p')), set)

    def test__neighbors__2(self):
        edges = edges_.Edges([('p', 'q'), ('q', 'r'), ('s', 'r')])
        self.assertEqual(edges.neighbors('p'), set(('q',)))
        self.assertEqual(edges.neighbors('q'), set(('p','r')))
        self.assertEqual(edges.neighbors('r'), set(('q','s')))
        self.assertEqual(edges.neighbors('s'), set(('r',)))

    def test__neighbors__KeyError(self):
        edges = edges_.Edges([('p', 'q')])
        with self.assertRaises(KeyError) as context:
            edges.neighbors('n0')
        self.assertEqual(repr('n0'), str(context.exception))

    def test__outward__1(self):
        edges = edges_.Edges([('p', 'q')])
        self.assertEqual(type(edges.outward('p')), set)

    def test__outward__2(self):
        edges = edges_.Edges([('p', 'q'), ('q', 'r'), ('s', 'r')])
        self.assertEqual(edges.outward('p'), set([('p','q'),]))
        self.assertEqual(edges.outward('q'), set([('q','r'),]))
        self.assertEqual(edges.outward('r'), set())
        self.assertEqual(edges.outward('s'), set([('s','r'),]))

    def test__outward__KeyError(self):
        edges = edges_.Edges([('p', 'q')])
        with self.assertRaises(KeyError) as context:
            edges.outward('n0')
        self.assertEqual(repr('n0'), str(context.exception))

    def test__inward__1(self):
        edges = edges_.Edges([('p', 'q')])
        self.assertEqual(type(edges.inward('p')), set)

    def test__inward__2(self):
        edges = edges_.Edges([('p', 'q'), ('q', 'r'), ('s', 'r')])
        self.assertEqual(edges.inward('p'), set())
        self.assertEqual(edges.inward('q'), set([('p','q'),]))
        self.assertEqual(edges.inward('r'), set([('q','r'), ('s','r')]))
        self.assertEqual(edges.inward('s'), set())

    def test__inward__KeyError(self):
        edges = edges_.Edges([('p', 'q')])
        with self.assertRaises(KeyError) as context:
            edges.inward('n0')
        self.assertEqual(repr('n0'), str(context.exception))

    def test__incident__1(self):
        edges = edges_.Edges([('p', 'q')])
        self.assertEqual(type(edges.incident('p')), set)

    def test__incident__2(self):
        edges = edges_.Edges([('p', 'q'), ('q', 'r'), ('s', 'r')])
        self.assertEqual(edges.incident('p'), set([('p','q')]))
        self.assertEqual(edges.incident('q'), set([('p','q'), ('q','r')]))
        self.assertEqual(edges.incident('r'), set([('q','r'), ('s','r')]))
        self.assertEqual(edges.incident('s'), set([('s','r')]))

    def test__incident__KeyError(self):
        edges = edges_.Edges([('p', 'q')])
        with self.assertRaises(KeyError) as context:
            edges.incident('n0')
        self.assertEqual(repr('n0'), str(context.exception))

    def test__adjacent__1(self):
        self.assertEqual(edges_.Edges.adjacent('p', ('p', 'q')), 'q')
        self.assertEqual(edges_.Edges.adjacent('q', ('p', 'q')), 'p')

    def test__adjacent__2(self):
        self.assertEqual(edges_.Edges.adjacent('p', ['p', 'q']), 'q')
        self.assertEqual(edges_.Edges.adjacent('q', ['p', 'q']), 'p')

    def test__adjacent__KeyError(self):
        with self.assertRaises(KeyError) as context:
            edges_.Edges.adjacent('r', ('p', 'q'))
        self.assertEqual(repr('r'), str(context.exception))

    def test__adjacent__ValueError_1(self):
        with self.assertRaises(ValueError) as context:
            edges_.Edges.adjacent('r', ('p',))
##        self.assertIn("not enough values to unpack", str(context.exception))

    def test__adjacent__ValueError_2(self):
        with self.assertRaises(ValueError) as context:
            edges_.Edges.adjacent('r', ('p','q','r'))
##        self.assertIn("too many values to unpack", str(context.exception))

    def test__contains__1(self):
        edges = edges_.Edges([('p', 'q'), ('q', 'r')])
        self.assertIn(('p','q'), edges)
        self.assertIn(('q','r'), edges)

    def test__contains__2(self):
        edges = edges_.Edges([('p', 'q'), ('q', 'r')])
        self.assertIn(['p','q'], edges)
        self.assertIn(['q','r'], edges)

    def test__contains__3(self):
        edges = edges_.Edges([('p', 'q'), ('q', 'r')])
        self.assertNotIn(('p','r'), edges)
        self.assertNotIn(('t','q'), edges) # must not throw

    def test__contains__4(self):
        edges = edges_.Edges([('p', 'q'), ('q', 'r')])
        self.assertNotIn(('p','r'), edges)
        self.assertNotIn(('p',), edges)            # must not throw
        self.assertNotIn(('p','q', 'r'), edges)  # must not throw

    def test__contains__5(self):
        edges = edges_.Edges({('p', 'q'): 'E1', ('q', 'r'): 'E2'})
        self.assertNotIn('E1', edges)
        self.assertNotIn('E2', edges)

    def test__contains__6(self):
        edges = edges_.Edges([('p', 'q'), ('r', 's')])
        self.assertIn('pq', edges) # yes, quite strange, so I just warn you here...
        self.assertIn('rs', edges) # yes, quite strange, so I just warn you here...

    def test__contains__7(self):
        edges = edges_.Edges(['pq', 'rs']) # yes, quite strange, so I just warn you here...
        self.assertIn('pq', edges) # yes, quite strange, so I just warn you here...
        self.assertIn('rs', edges) # yes, quite strange, so I just warn you here...

    def test__iter__(self):
        edges = edges_.Edges({('p','q'): 'E1', ('q','r'): 'E2'})
        self.assertEqual(list(iter(edges)), list(iter(edges.data)))

    def test__len__(self):
        edges = edges_.Edges({('p','q'): 'E1', ('q','r'): 'E2'})
        self.assertEqual(len(edges), 2)

    def test__repr__1(self):
        edges = edges_.Edges({('p','q'): 'E1', ('q','r'): 'E2'})
        self.assertEqual(repr(edges), "Edges(%s)" % repr(edges.data))

    def test__repr__2(self):
        edges = edges_.Edges()
        self.assertEqual(repr(edges), "Edges()")

    def test__getitem__1(self):
        edges = edges_.Edges({('p','q'): 'E1', ('q','r'): 'E2'})
        self.assertEqual(edges[('p','q')],'E1')
        self.assertEqual(edges[('q','r')],'E2')

    def test__getitem__2(self):
        edges = edges_.Edges({('p','q'): 'E1', ('r','s'): 'E2'})
        self.assertEqual(edges['pq'],'E1')
        self.assertEqual(edges['rs'],'E2')

    def test__getitem__KeyError_1(self):
        edges = edges_.Edges()
        with self.assertRaises(KeyError) as context:
            edges[('p', 'q')]
        self.assertEqual(repr(('p', 'q')), str(context.exception))

    def test__getitem__KeyError_2(self):
        edges = edges_.Edges()
        with self.assertRaises(KeyError) as context:
            edges[['p', 'q']]
        self.assertEqual(repr(['p', 'q']), str(context.exception))

    def test__getitem__KeyError_3(self):
        edges = edges_.Edges()
        with self.assertRaises(KeyError) as context:
            edges['pq']
        self.assertEqual(repr('pq'), str(context.exception))

    def test__getitem__KeyError_4(self):
        edges = edges_.Edges([('p','q'), ('q','r')])
        with self.assertRaises(KeyError) as context:
            edges[('p',)]
        self.assertEqual(repr(('p',)), str(context.exception))

    def test__getitem__KeyError_5(self):
        edges = edges_.Edges([('p','q'), ('q','r')])
        with self.assertRaises(KeyError) as context:
            edges[('p','q','r')]
        self.assertEqual(repr(('p','q','r')), str(context.exception))

    def test__setitem__1(self):
        edges = edges_.Edges({('p','q'):  'E1'})
        edges[('p','q')] = '_E1_'
        self.assertEqual(edges.data, {('p','q'):  '_E1_'})
        self.assertEqual(edges.successors_dict, {'p':  set(('q',))})
        self.assertEqual(edges.predecessors_dict, {'q':  set(('p',))})

    def test__setitem__2(self):
        edges = edges_.Edges({('p','q'):  'E1'})
        edges[('p','q')] = '_E1_'
        edges[('q','r')] = '_E2_'
        self.assertEqual(edges.data, {('p','q'):  '_E1_', ('q','r'):  '_E2_'})
        self.assertEqual(edges.successors_dict, {'p':  set(('q',)), 'q':  set(('r',))})
        self.assertEqual(edges.predecessors_dict, {'q':  set(('p',)), 'r':  set(('q',))})

    def test__setitem__ValueError_1(self):
        edges = edges_.Edges()
        with self.assertRaises(ValueError) as context:
            edges[('p',)] = 'E1'
##        self.assertIn("not enough values to unpack", str(context.exception))
        self.assertEqual(edges.data, dict())
        self.assertEqual(edges.successors_dict, dict())
        self.assertEqual(edges.predecessors_dict, dict())

    def test__setitem__ValueError_2(self):
        edges = edges_.Edges()
        with self.assertRaises(ValueError) as context:
            edges[('p','q','r')] = 'E1'
##        self.assertIn("too many values to unpack", str(context.exception))
        self.assertEqual(edges.data, dict())
        self.assertEqual(edges.successors_dict, dict())
        self.assertEqual(edges.predecessors_dict, dict())

    def test__delitem__1(self):
        edges = edges_.Edges({('p','q'): 'E1', ('q','r'): 'E2'})
        del edges[('p','q')]
        self.assertEqual(edges.data, {('q','r'):  'E2'})
        self.assertEqual(edges.successors_dict, {'q':  set(('r',))})
        self.assertEqual(edges.predecessors_dict, {'r':  set(('q',))})

    def test__delitem__KeyError_1(self):
        edges = edges_.Edges({('p','q'): 'E1', ('q','r'): 'E2'})
        with self.assertRaises(KeyError) as context:
            del edges[('r','p')]
        self.assertEqual(repr(('r','p')), str(context.exception))
        self.assertEqual(edges.data, {('p','q'):  'E1', ('q','r'):  'E2'})
        self.assertEqual(edges.successors_dict, {'p':  set(('q',)), 'q':  set(('r',))})
        self.assertEqual(edges.predecessors_dict, {'q':  set(('p',)), 'r':  set(('q',))})

    def test__delitem__KeyError_2(self):
        edges = edges_.Edges({('p','q'): 'E1', ('q','r'): 'E2'})
        with self.assertRaises(KeyError) as context:
            del edges[('q','p')]
        self.assertEqual(repr(('q','p')), str(context.exception))
        self.assertEqual(edges.data, {('p','q'):  'E1', ('q','r'):  'E2'})
        self.assertEqual(edges.successors_dict, {'p':  set(('q',)), 'q':  set(('r',))})
        self.assertEqual(edges.predecessors_dict, {'q':  set(('p',)), 'r':  set(('q',))})

    def test__delitem__KeyError_3(self):
        edges = edges_.Edges({('p','q'): 'E1', ('q','r'): 'E2'})
        with self.assertRaises(KeyError) as context:
            del edges[('p',)]
        self.assertEqual(repr(('p',)), str(context.exception))
        self.assertEqual(edges.data, {('p','q'):  'E1', ('q','r'):  'E2'})
        self.assertEqual(edges.successors_dict, {'p':  set(('q',)), 'q':  set(('r',))})
        self.assertEqual(edges.predecessors_dict, {'q':  set(('p',)), 'r':  set(('q',))})

    def test__delitem__KeyError_4(self):
        edges = edges_.Edges({('p','q'): 'E1', ('q','r'): 'E2'})
        with self.assertRaises(KeyError) as context:
            del edges[('p','q','r')]
        self.assertEqual(repr(('p','q','r')), str(context.exception))
        self.assertEqual(edges.data, {('p','q'):  'E1', ('q','r'):  'E2'})
        self.assertEqual(edges.successors_dict, {'p':  set(('q',)), 'q':  set(('r',))})
        self.assertEqual(edges.predecessors_dict, {'q':  set(('p',)), 'r':  set(('q',))})

    def test__add__1(self):
        edges = edges_.Edges({('p','q'):  'E1'})
        edges.add(('p','q'), '_E1_')
        edges.add(('q','r'), '_E2_')
        self.assertEqual(edges.data, {('p','q'):  '_E1_', ('q','r'):  '_E2_'})
        self.assertEqual(edges.successors_dict, {'p':  set(('q',)), 'q':  set(('r',))})
        self.assertEqual(edges.predecessors_dict, {'q':  set(('p',)), 'r':  set(('q',))})

    def test__add__2(self):
        edges = edges_.Edges({('p','q'):  'E1'})
        edges.add(('p','q'))
        edges.add(('q','r'))
        self.assertEqual(edges.data, {('p','q'):  'E1', ('q','r'):  None})
        self.assertEqual(edges.successors_dict, {'p':  set(('q',)), 'q':  set(('r',))})
        self.assertEqual(edges.predecessors_dict, {'q':  set(('p',)), 'r':  set(('q',))})

    def test__add__ValueError_1(self):
        edges = edges_.Edges()
        with self.assertRaises(ValueError) as context:
            edges.add(('p',))
##        self.assertIn("not enough values to unpack", str(context.exception))
        self.assertEqual(edges.data, dict())
        self.assertEqual(edges.successors_dict, dict())
        self.assertEqual(edges.predecessors_dict, dict())

    def test__add__ValueError_2(self):
        edges = edges_.Edges()
        with self.assertRaises(ValueError) as context:
            edges.add(('p','q','r'))
##        self.assertIn("too many values to unpack", str(context.exception))
        self.assertEqual(edges.data, dict())
        self.assertEqual(edges.successors_dict, dict())
        self.assertEqual(edges.predecessors_dict, dict())

    def test__discard__1(self):
        edges = edges_.Edges({('p','q'): 'E1', ('q','r'): 'E2'})
        edges.discard(('p','q'))
        self.assertEqual(edges.data, {('q','r'):  'E2'})
        self.assertEqual(edges.successors_dict, {'q':  set(('r',))})
        self.assertEqual(edges.predecessors_dict, {'r':  set(('q',))})

    def test__discard__2(self):
        edges = edges_.Edges({('p','q'): 'E1', ('q','r'): 'E2'})
        edges.discard(('r','p'))
        self.assertEqual(edges.data, {('p','q'):  'E1', ('q','r'):  'E2'})
        self.assertEqual(edges.successors_dict, {'p':  set(('q',)), 'q':  set(('r',))})
        self.assertEqual(edges.predecessors_dict, {'q':  set(('p',)), 'r':  set(('q',))})

    def test__clear(self):
        edges = edges_.Edges({('p','q'): 'E1', ('q','r'): 'E2'})
        edges.clear()
        self.assertEqual(edges.data, dict())
        self.assertEqual(edges.successors_dict, dict())
        self.assertEqual(edges.predecessors_dict, dict())

    def test__items(self):
        edges = edges_.Edges({('p','q'): 'E1', ('q','r'): 'E2'})
        self.assertEqual(list(edges.items()), list(edges.data.items()))

    def test__del_incident__1(self):
        edges = edges_.Edges([('p','q'), ('q','r'), ('s', 'q')])
        edges.del_incident('s')
        self.assertEqual(edges.data, {('p','q'):  None, ('q','r'):  None})
        self.assertEqual(edges.successors_dict, {'p':  set(('q',)), 'q':  set(('r',))})
        self.assertEqual(edges.predecessors_dict, {'q':  set(('p',)), 'r':  set(('q',))})

    def test__del_incident__2(self):
        edges = edges_.Edges([('p','q'), ('q','r'), ('s', 'q')])
        edges.del_incident('q')
        self.assertEqual(edges.data, dict())
        self.assertEqual(edges.successors_dict, dict())
        self.assertEqual(edges.predecessors_dict, dict())

    def test__del_incident__3(self):
        edges = edges_.Edges([('p','q'), ('q','r'), ('s', 'r')])
        edges.del_incident('r')
        self.assertEqual(edges.data, {('p','q'):  None})
        self.assertEqual(edges.successors_dict, {'p':  set(('q',))})
        self.assertEqual(edges.predecessors_dict, {'q':  set(('p',))})

    def test__del_incident__KeyError(self):
        edges = edges_.Edges([('p','q'), ('q','r')])
        with self.assertRaises(KeyError) as context:
            edges.del_incident('s')
        self.assertEqual(repr('s'), str(context.exception))

if __name__ == '__main__':
    unittest.main()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
