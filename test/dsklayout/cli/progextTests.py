#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest
import unittest.mock as mock

import dsklayout.cli.progext_ as progext_
import dsklayout.cli.ext_ as ext_


class Test__CliTmpdirExt(unittest.TestCase):

    def test__isinstance__CliExt(self):
        ext = progext_.ProgExt('foo')
        self.assertIsInstance(ext, ext_.CliExt)

    def test__name(self):
        ext = progext_.ProgExt('foo')
        self.assertEqual('foo', ext.name)

    def test__properties__00(self):
        ext = progext_.ProgExt('foo')
        self.assertEqual('--foo', ext.prog_option)
        self.assertEqual('foo', ext.prog_dest)
        self.assertEqual('foo', ext.prog_default)
        self.assertEqual('path to foo program', ext.prog_help)
        self.assertEqual('foo', ext.prog_name)

    def test__properties__01(self):
        ext = progext_.ProgExt('foo', prog_option='--foo-option', prog_dest='foo_dest', prog_default='default-foo', prog_help='FOO help', prog_name='fooname')
        self.assertEqual('--foo-option', ext.prog_option)
        self.assertEqual('foo_dest', ext.prog_dest)
        self.assertEqual('default-foo', ext.prog_default)
        self.assertEqual('FOO help', ext.prog_help)
        self.assertEqual('fooname', ext.prog_name)

    def test__add_arguments(self):
        ext = progext_.ProgExt('foo')
        parser = mock.Mock(spec =[])
        with mock.patch.object(ext, 'add_prog_argument') as add_prog_argument:
            ext.add_arguments(parser)
            add_prog_argument.assert_called_once_with(parser)

    def test__add_prog_argument__00(self):
        ext = progext_.ProgExt('foo')
        parser = mock.Mock(spec =[])
        parser.add_argument = mock.Mock()
        self.assertIsNone(ext.add_prog_argument(parser))
        parser.add_argument.assert_has_calls([
            mock.call("--foo", dest='foo', metavar='PROG', default='foo', help="path to foo program")
        ])

    def test__add_prog_argument__01(self):
        ext = progext_.ProgExt('foo', prog_option='--foo-option', prog_dest='foo_dest', prog_default='default-foo', prog_help='FOO help', prog_name='fooname')
        parser = mock.Mock(spec =[])
        parser.add_argument = mock.Mock()
        self.assertIsNone(ext.add_prog_argument(parser))
        parser.add_argument.assert_has_calls([
            mock.call("--foo-option", dest='foo_dest', metavar='PROG', default='default-foo', help="FOO help")
        ])



if __name__ == '__main__':
    unittest.main()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
