import os
import sys

import yaml

from wheeljack import DEFAULT_CONFIG
from wheeljack.exceptions import ReposConfigException

__config = None


def _clear_cache():
    """Clear the config cache."""
    global __config
    __config = None


def get_config_filename():
    """Gets the configuration file which defines all the repos we might want."""
    return os.environ.get('WHEELJACK_CONFIG', DEFAULT_CONFIG)


def get_config(config):
    """Gets the configuration.

    :param config: if config is set just use it.
    :return: a dictionary of configuration data.
    :raise: ReposConfigException if the file cannot be opened.
    """

    global __config
    if __config:
        return __config

    if config:
        __config = config

    else:
        try:
            with open(get_config_filename(), 'r') as stream:
                __config = yaml.load(stream)
        except IOError:
            raise ReposConfigException("{} could not be opened.".format(
                get_config_filename()
            ))

    for _, data in __config['repos'].iteritems():
        host = data.get('host', __config.get('global', {}).get(
            'host', 'github.com'))
        data['url'] = 'git@{}:{}.git'.format(host, data.get('source'))
    return __config


def _list_repos(config=None):
    config = get_config(config)
    return sorted(config.get('repos').iterkeys())


def list_repos(config=None):
    try:
        return _list_repos(config)
    except ReposConfigException as e:
        sys.stderr.write(e.message + '\n')
        sys.stderr.write('You can override this by setting the WHEELJACK_CONFIG'
                         ' environment variable.\n')
        exit(-1)
