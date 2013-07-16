__author__ = 'davedash'


class WheeljackException(Exception):
    pass


class RepoNotFoundException(WheeljackException):
    """Exception thrown when we interact with an undefined Repo."""
    pass


class RepoAlreadyInstalledException(WheeljackException):
    """Exception thrown when we try to re-install a repo."""
    pass


class ReposConfigException(WheeljackException):
    """Exception raised when there is a configuration error."""
    pass


class WheeljackCodeDirectoryMissing(WheeljackException):
    """Raised if we are missing our base directory."""
    pass


class GitNotRepoException(WheeljackException):
    """Raise if we interact with a non Git-dir in a Git-ish manner."""
    pass


class GitNoOriginRemoteException(WheeljackException):
    pass
