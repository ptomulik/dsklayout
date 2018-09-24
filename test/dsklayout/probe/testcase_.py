#!/usr/bin/env python3
# -*- coding: utf8 -*-

import os
import os.path
import unittest


class ProbeTestCase(unittest.TestCase):

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self._fixtures = dict()

    def tearDown(self):
        self._fixtures = dict() # cleanup used fixtures

    @property
    def fixture_plan(self):
        return []

    @property
    def fixtures(self):
        if not self._fixtures:
            self.load_fixtures()
        return self._fixtures

    def load_fixtures(self):
        for left, right in self.fixture_plan:
            with open(self.fixture_path(left)) as f:
                self._fixtures[left] = self.decode_left_fixture(f.read())
            with open(self.fixture_path(right)) as f:
                self._fixtures[right] = self.decode_right_fixture(f.read())

    def fixture_path(self, file):
        mydir = os.path.dirname(__file__)
        return os.path.join(mydir, 'fixtures', file)

    def decode_left_fixture(self, content):
        return content

    def decode_right_fixture(self, content):
        return content

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set ft=python et ts=4 sw=4:
