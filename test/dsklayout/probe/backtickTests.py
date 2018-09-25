#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unittest
import dsklayout.probe.backtick_ as backtick_
import dsklayout.probe.probe_ as probe_
from unittest.mock import patch

backtick = 'dsklayout.util.backtick'

def there(member=None):
    if member is None:
        return 'dsklayout.probe.backtick_.BackTickProbe'
    else:
        return 'dsklayout.probe.backtick_.BackTickProbe.%s' % member

class Test__BackTickProbe(unittest.TestCase):

    def test__is_subclass_of_Probe(self):
        self.assertTrue(issubclass(backtick_.BackTickProbe, probe_.Probe))

    def test__is_abstract(self):

        with self.assertRaises(TypeError) as context:
            backtick_.BackTickProbe({})

        self.assertIn("abstract", str(context.exception))

    def test__subclassing(self):
        class T(backtick_.BackTickProbe):
            @classmethod
            def cmdname(cls):
                return 'foo'
            @classmethod
            def parse(cls, output):
                return super().parse(output)
            @classmethod
            def flags(cls, flags=None, **kw):
                return super().flags(flags, **kw)

        self.assertEqual(T.command(), 'foo')
        self.assertEqual(T.command(foo='bar'), 'bar')
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
             patch(there('cmdname'), return_value='doit') as command:
            content = backtick_.BackTickProbe.run()
            mock.assert_called_once_with(['doit'])
            self.assertEqual(content, 'ok')

    def test__run__2(self):
        with patch(backtick, return_value='ok') as mock, \
             patch(there('cmdname'), return_value='doit') as command:
            content = backtick_.BackTickProbe.run(['arg1', 'arg2'], ['-f1', '-f2'])
            mock.assert_called_once_with(['doit', 'arg1', 'arg2'])
            self.assertEqual(content, 'ok')

    def test__new__1(self):
        class T(backtick_.BackTickProbe):
            @classmethod
            def cmdname(cls):
                return 'doit'
            @classmethod
            def parse(cls, output):
                return output + ' parsed'
        with patch.object(T, 'run', return_value='ok') as run:
            obj = T.new()
            run.assert_called_once_with(None, None)
            self.assertIsInstance(obj, T)
            self.assertEqual(obj.content, 'ok parsed')

    def test__which__1(self):
        class T(backtick_.BackTickProbe):
            @classmethod
            def cmdname(cls):
                return 'doit'
        with patch('shutil.which', return_value='ok') as which:
            self.assertIs(T.which(), 'ok')
            which.assert_called_once_with('doit')

    def test__which__2(self):
        class T(backtick_.BackTickProbe):
            @classmethod
            def cmdname(cls):
                return 'doit'
            @classmethod
            def command(cls, **kw):
                return cls.cmdname() + kw['suffix']
        with patch('shutil.which', return_value='ok') as which:
            self.assertIs(T.which(suffix='-now'), 'ok')
            which.assert_called_once_with('doit-now')

    def test__available__1(self):
        class T(backtick_.BackTickProbe):
            @classmethod
            def cmdname(cls):
                return 'doit'
            @classmethod
            def command(cls, **kw):
                return cls.cmdname() + kw['suffix']
        with patch('dsklayout.probe.backtick_.BackTickProbe.which', return_value='ok') as which:
            self.assertTrue(T.available(suffix='-now'))
            which.assert_called_once_with(suffix='-now')

    def test__available__2(self):
        class T(backtick_.BackTickProbe):
            @classmethod
            def cmdname(cls):
                return 'doit'
            @classmethod
            def command(cls, **kw):
                return cls.cmdname() + kw['suffix']
        with patch('dsklayout.probe.backtick_.BackTickProbe.which', return_value=None) as which:
            self.assertFalse(T.available(suffix='-now'))
            which.assert_called_once_with(suffix='-now')



if __name__ == '__main__':
    unittest.main()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
