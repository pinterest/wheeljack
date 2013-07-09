import os
from unittest import TestCase

from nose.tools import eq_

from wheeljack import DEFAULT_CONFIG
from wheeljack.config import get_config

__author__ = 'davedash'


class GetConfigTestCase(TestCase):
    def test_get_config(self):
        """Test that `get_config` returns the default config."""
        eq_(DEFAULT_CONFIG, get_config())

    def test_get_config_override(self):
        """Test that `get_config` returns the overridden config."""
        expected = '/tmp/foo'
        os.environ['WHEELJACK_CONFIG'] = expected
        eq_(expected, get_config())
