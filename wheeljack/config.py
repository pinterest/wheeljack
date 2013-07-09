import os
import sys

import yaml

from wheeljack import DEFAULT_CONFIG


def get_config():
    """Gets the configuration file which defines all the repos we might want."""
    return os.environ.get('WHEELJACK_CONFIG', DEFAULT_CONFIG)


def _list_repos(config=None):
    if not config:
        try:
            with file(get_config(), 'r') as stream:
                config = yaml.load(stream)
        except IOError:
            raise ReposConfigException("{} could not be opened.".format(
                get_config()
            ))
    return sorted(config.get('repos').iterkeys())


def list_repos(config=None):
    try:
        return _list_repos(config)
    except ReposConfigException as e:
        sys.stderr.write(e.message + '\n')
        sys.stderr.write('You can override this by setting the WHEELJACK_CONFIG'
                         ' environment variable.\n')
        exit(-1)


class ReposConfigException(Exception):
    pass
