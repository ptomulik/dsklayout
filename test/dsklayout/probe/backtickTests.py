#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest
import dsklayout.probe.backtick_ as backtick_
import dsklayout.probe.probe_ as probe_
from unittest.mock import patch

backtick = 'dsklayout.util.backtick'

class Test__BackTickProbe(unittest.TestCase):

    def test__subclass__1(self):
        self.assertTrue(issubclass(backtick_.BackTickProbe, probe_.Probe))

    def test__abstract__1(self):

        with self.assertRaises(TypeError) as context:
            backtick_.BackTickProbe()

        self.assertIn("abstract", str(context.exception))

    def test__derived__1(self):
        class T(backtick_.BackTickProbe):
            @classmethod
            def command(cls, **kw):
                return super().command(**kw)
            @classmethod
            def parse(cls, output):
                return super().parse(output)
            @classmethod
            def flags(cls, flags=None, **kw):
                return super().flags(flags, **kw)

        self.assertIsNone(T.command())
        self.assertIsNone(T.parse("output"))
        self.assertEqual(T.flags(), [])

    def test__kwargs__1(self):
        popen_kwargs = {
            'bufsize': 'BUFSIZE',
            'executable': 'EXECUTABLE',
            'stdin': 'STDIN',
            'stdout': 'STDOUT',
            'preexec_fn': 'PREEXEC_FN',
            'close_fds': 'CLOSE_FDS',
            'shell': 'SHELL',
            'cwd': 'CWD',
            'env': 'ENV',
            'universal_newlines': 'UNIVERSAL_NEWLINES',
            'startupinfo': 'STARTUPINFO',
            'creationflags': 'CREATIONFLAGS',
            'restore_signals': 'RESTORE_SIGNALS',
            'start_new_session': 'START_NEW_SESSION',
            'pass_fds': 'PASS_FDS',
            'encoding': 'ENCODING',
            'errors': 'ERRORS'
        }
        test_kwargs = dict(popen_kwargs, **{'foo': 'FOO'})
        kwargs = backtick_.BackTickProbe.kwargs(**test_kwargs)
        self.assertEqual(kwargs, popen_kwargs)

    def test__run__1(self):
        with patch(backtick, return_value='ok') as mock, \
             patch.object(backtick_.BackTickProbe, 'command', return_value='doit') as command:
            content = backtick_.BackTickProbe.run()
            mock.assert_called_once_with(['doit'])
            self.assertEqual(content, 'ok')

    def test__run__2(self):
        with patch(backtick, return_value='ok') as mock, \
             patch.object(backtick_.BackTickProbe, 'command', return_value='doit') as command:
            content = backtick_.BackTickProbe.run(['arg1', 'arg2'], ['-f1', '-f2'])
            mock.assert_called_once_with(['doit', 'arg1', 'arg2'])
            self.assertEqual(content, 'ok')

    def test__new__1(self):
        class T(backtick_.BackTickProbe):
            @classmethod
            def command(cls, **kw):
                return 'doit'
            @classmethod
            def parse(cls, output):
                return output + ' parsed'
        with patch.object(T, 'run', return_value='ok') as run:
            obj = T.new()
            run.assert_called_once_with(None, None)
            self.assertIsInstance(obj, T)
            self.assertEqual(obj.content, 'ok parsed')


if __name__ == '__main__':
    unittest.main()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
