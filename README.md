[![Build Status](https://travis-ci.org/pinterest/wheeljack.png?branch=master)](https://travis-ci.org/pinterest/wheeljack)

# Wheeljack

Wheeljack helps manage dependent python projects.  All related projects will
live in `$WHEELJACK_REPO` and will interact with one another in the active
virtual environment.

E.g. you may have a directory structure:

```
$WHEELJACK_REPO/
    foo/
    bar/

```

Where `foo` and `bar` are both python packages.  In this environment you should
be able to freely edit `foo` or `bar` and access one another by doing `import
foo` or `import bar`.  If you also do:

```
pip install bar
```

Your environment should favor the `git` working copy of `bar` over the `pip
install`ed package.  This will allow you to work on packages and their
dependencies fairly seemlessly.

Wheeljack expects you to use a `virtualenv`.

## repos.conf

This is a `yaml` file which lists repositories in Github or Github Enterprise.

There are two main parts of the config.  `global` which applies to all `repos`
and `repos` which define individual repositories.

See `example.conf`.

## install-repo

`install-repo` will install a repo from a repos.conf file to `$WHEELJACK_CODE`.
We'll instruct the user to use the `hub` command to fork this repo.

## TODO

* `update-libs` will update the current virtualenv:
  * It will `git fetch origin/master` on any repos in `$WHEELJACK_CODE`
  * It will `pip install -r $WHEELJACK_CODE/**/requirements.txt` for every
    installed requirement.
* Work with multiple python `virutalenv`s.
