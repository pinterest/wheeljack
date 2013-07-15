import os

from nose.tools import eq_
import yaml
from tests import DUMMY_CONFIG, TestCase

from wheeljack import DEFAULT_CONFIG
from wheeljack.config import (_list_repos, get_config_filename, list_repos,
                              get_config, _clear_cache)
from wheeljack.exceptions import ReposConfigException

__author__ = 'davedash'


class GetConfigFilenameTestCase(TestCase):
    def test_get_config_filename(self):
        """Test that `get_config_filename` returns the default config."""
        eq_(DEFAULT_CONFIG, get_config_filename())

    def test_get_config_filename_override(self):
        """Test that `get_config_filename` returns the overridden config."""
        expected = '/tmp/foo'
        os.environ['WHEELJACK_CONFIG'] = expected
        eq_(expected, get_config_filename())


class GetConfigTestCase(TestCase):
    def test_get_config_adds_url(self):
        """Test that `get_config` adds a url to a repo correctly."""
        config = get_config(yaml.load(DUMMY_CONFIG))
        expect = "git@github.com:davedash/wheeljack.git"
        eq_(expect, config['repos']['wheeljack']['url'])


class ListReposTestCase(TestCase):


    def test_list_repos(self):
        expected = ['nuggets', 'wheeljack']
        config = yaml.load(DUMMY_CONFIG)
        eq_(expected, list_repos(config))

    def test__list_repos_exception(self):
        """Raise an exception if we can't open the config."""
        os.environ['WHEELJACK_CONFIG'] = "/asdf"
        self.assertRaises(ReposConfigException, _list_repos)
