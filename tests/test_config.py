import os
from unittest import TestCase

from nose.tools import eq_
import yaml

from wheeljack import DEFAULT_CONFIG
from wheeljack.config import (_list_repos, get_config, list_repos,
                              ReposConfigException)

__author__ = 'davedash'


dummy_config = """
global:
    host: github.com
repos:
  wheeljack:
    source: davedash/wheeljack
  nuggets:
    source: Pinterest/nuggets
"""


class GetConfigTestCase(TestCase):
    def test_get_config(self):
        """Test that `get_config` returns the default config."""
        eq_(DEFAULT_CONFIG, get_config())

    def test_get_config_override(self):
        """Test that `get_config` returns the overridden config."""
        expected = '/tmp/foo'
        os.environ['WHEELJACK_CONFIG'] = expected
        eq_(expected, get_config())


class ListReposTestCase(TestCase):
    def test_list_repos(self):
        expected = ['nuggets', 'wheeljack']
        config = yaml.load(dummy_config)
        eq_(expected, list_repos(config))

    def test__list_repos_exception(self):
        """Raise an exception if we can't open the config."""
        os.environ['WHEELJACK_CONFIG'] = "/asdf"
        self.assertRaises(ReposConfigException, _list_repos)
