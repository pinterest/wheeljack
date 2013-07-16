import os
import re
import subprocess

from blessings import Terminal
from wheeljack import INDENT

from wheeljack.config import list_repos, get_config
from wheeljack.exceptions import (
    RepoNotFoundException, RepoAlreadyInstalledException,
    WheeljackCodeDirectoryMissing, GitNotRepoException,
    GitNoOriginRemoteException)

__author__ = 'davedash'

terminal = Terminal()


def __git_command(url):
    """Checks out a git URL.

    Returns newly created directory.
    """
    dir_ = get_code_dir(url)
    subprocess.check_call(('git', 'clone', url, dir_))
    return dir_


def _install_repo(repo, config=None, git_command=None):
    repos = list_repos(config)
    config = get_config(config)
    if repo not in repos:
        raise RepoNotFoundException

    data = config['repos'][repo]

    if not git_command:
        git_command = __git_command

    url = data['url']
    code_dir = get_code_dir(url)
    if os.path.exists(code_dir):
        raise RepoAlreadyInstalledException(
            "Something already exists in {}.  "
            "What more do you want?".format(code_dir))

    if not os.path.exists(_get_code_base_dir()):
        raise WheeljackCodeDirectoryMissing
    return git_command(url)


def _fork_and_add_remote(dir_):
    if not os.path.exists(os.path.join(dir_, '.git')):
        raise GitNotRepoException
    if not os.path.exists(os.path.join(dir_, '.git/refs/remotes/origin')):
        raise GitNoOriginRemoteException
    print terminal.cyan("You may now fork the repository by using hub:")
    print
    print INDENT, "cd {}".format(dir_)
    print INDENT, "hub fork"


def install_repo(repo, config=None, git_command=None):
    try:
        dir_ = _install_repo(repo, config, git_command)
        _fork_and_add_remote(dir_)
        os.chdir(dir_)
        return dir_

    except WheeljackCodeDirectoryMissing:
        print ("{t.red}Sorry I could not clone {} for you.  "
               "{} is missing.").format(repo, _get_code_base_dir(), t=terminal)

        print "{t.cyan}Create it with:{t.normal}".format(
            _get_code_base_dir(), t=terminal)
        print "\n    mkdir {}".format(_get_code_base_dir())
        print "\n{t.cyan}Or override it with:{t.normal}".format(t=terminal)
        print "\n    export WHEELJACK_CODE={directory}"
        exit(1)

    except RepoAlreadyInstalledException as e:
        print "{t.yellow}{}{t.normal}".format(e.message, t=terminal)


def _get_code_base_dir():
    base = os.environ.get('WHEELJACK_CODE', os.path.expanduser('~/code'))
    return base


def get_code_dir(url):
    path = re.search(r'git@.*:.*?([^\/]+).git', url).groups()[0]
    return os.path.join(_get_code_base_dir(), path)