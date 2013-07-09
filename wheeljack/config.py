import os

from wheeljack import DEFAULT_CONFIG


def get_config():
    """Gets the configuration file which defines all the repos we might want."""
    return os.environ.get('WHEELJACK_CONFIG', DEFAULT_CONFIG)
