import os
import subprocess

from nose.tools import eq_, ok_
import yaml

from wheeljack.exceptions import (
    RepoNotFoundException, RepoAlreadyInstalledException,
    WheeljackCodeDirectoryMissing, GitNotRepoException,
    GitNoOriginRemoteException)
from wheeljack.install import (
    _install_repo, install_repo, _get_code_dir_from_url, _fork_and_add_remote,
    _create_pth, _get_venv_or_create)

from tests import DUMMY_CONFIG, TestCase


def mock_git_command(url):
    dir_ = _get_code_dir_from_url(url)
    os.mkdir(dir_)
    return dir_


class GetCodeDirTestCase(TestCase):
    def test_get_code_dir(self):
        url = "git@github.whatever:Foo/BAR.git"
        expect = os.path.expanduser('~/code/BAR')
        eq_(expect, _get_code_dir_from_url(url))


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
        try:
            install_repo('nuggets', config=self.config,
                         git_command=mock_git_command)
        except GitNotRepoException:
            pass  # We are testing for something else.

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


def dummy_virtualenv(path):
    return os.makedirs(os.path.join(path, 'lib/python2.7/site-packages'))


class CreatePthTestCase(TestCase):
    def test_create_pth(self):
        """Should create a pth file.

        pth file should be .venv/**/site-packages/foo.pth
        """
        os.environ['WHEELJACK_CODE'] = self.tmp_dir
        new_dir = 'foo'
        _create_pth(new_dir, virtualenv_cmd=dummy_virtualenv)
        destination = '.venv/lib/python2.7/site-packages/foo.pth'
        ok_(os.path.exists(os.path.join(self.tmp_dir, destination)),
            ".pth file not created in {}".format(destination))
        with open(os.path.join(self.tmp_dir, destination)) as f:
            expect = 3
            reality = len(f.readlines())
            eq_(expect, reality,
                "Expected {} lines, got {}".format(expect, reality))

    def test_create_pth_existing_repo(self):
        """If there's an existing repo and no pth file we should create one."""
        os.environ['WHEELJACK_CODE'] = self.tmp_dir
        new_dir = os.path.join(self.tmp_dir, 'nuggets')
        os.mkdir(new_dir)
        config = yaml.load(DUMMY_CONFIG)
        install_repo('nuggets', config=config)
        destination = '.venv/lib/python2.7/site-packages/nuggets.pth'
        ok_(os.path.exists(os.path.join(self.tmp_dir, destination)),
            ".pth file not created in {}".format(destination))
        with open(os.path.join(self.tmp_dir, destination)) as f:
            expect = 3
            reality = len(f.readlines())
            eq_(expect, reality,
                "Expected {} lines, got {}".format(expect, reality))


class GetVenvOrCreateTestCase(TestCase):
    def test_get_env_or_create(self):
        """Creates a venv."""
        os.environ['WHEELJACK_CODE'] = self.tmp_dir
        expect = os.path.join(self.tmp_dir, '.venv')
        venv = _get_venv_or_create(dummy_virtualenv)
        eq_(expect, venv)
        # Test for idempotency.
        venv = _get_venv_or_create()
        eq_(expect, venv)
