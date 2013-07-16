import os
import subprocess

from nose.tools import eq_
import yaml

from wheeljack.exceptions import (
    RepoNotFoundException, RepoAlreadyInstalledException,
    WheeljackCodeDirectoryMissing, GitNotRepoException,
    GitNoOriginRemoteException)
from wheeljack.install import (_install_repo, install_repo, get_code_dir,
                               _fork_and_add_remote)

from tests import DUMMY_CONFIG, TestCase


def mock_git_command(url):
    dir_ = get_code_dir(url)
    os.mkdir(dir_)
    return dir_


class GetCodeDirTestCase(TestCase):
    def test_get_code_dir(self):
        url = "git@github.whatever:Foo/BAR.git"
        expect = os.path.expanduser('~/code/BAR')
        eq_(expect, get_code_dir(url))


class InstallRepoTestCase(TestCase):
    def setUp(self):
        super(InstallRepoTestCase, self).setUp()
        self.config = yaml.load(DUMMY_CONFIG)

    def test_invalid_repo(self):
        self.assertRaises(RepoNotFoundException, _install_repo, 'foo',
                          config=self.config)

    def test_valid_repo(self):
        code_dir = self.tmp_dir
        os.environ['WHEELJACK_CODE'] = code_dir
        install_repo('nuggets', config=self.config,
                     git_command=mock_git_command)

        # Let's make sure it creates a directory.
        self.assertTrue(os.path.exists(os.path.join(code_dir, 'nuggets')))

    def test_already_exists(self):
        code_dir = self.tmp_dir
        os.environ['WHEELJACK_CODE'] = code_dir
        nuggets_dir = os.path.join(code_dir, 'nuggets')
        os.mkdir(nuggets_dir)
        self.assertRaises(RepoAlreadyInstalledException, _install_repo,
                          'nuggets', config=self.config)

    def test_missing_base_dir(self):
        code_dir = os.path.join(self.tmp_dir, 'aabbbabab')
        os.environ['WHEELJACK_CODE'] = code_dir
        self.assertRaises(WheeljackCodeDirectoryMissing, _install_repo,
                          'nuggets', config=self.config)


class ForkAndAddRemoteTestCase(TestCase):
    """No good way to test the happy path since we don't really want to fork."""
    def test_not_git_repo(self):
        dir_ = self.tmp_dir
        self.assertRaises(GitNotRepoException, _fork_and_add_remote, dir_)

    def test_no_origin(self):
        dir_ = self.tmp_dir
        subprocess.check_output(('git', 'init', dir_))
        self.assertRaises(GitNoOriginRemoteException, _fork_and_add_remote, dir_)
