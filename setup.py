from setuptools import setup
import os

__version__ = '0.3'
markdown_contents = open(os.path.join(os.path.dirname(__file__),
                                      'README.md')).read()

setup(
    name='wheeljack-repoman',
    version= __version__,
    scripts=['bin/{}'.format(p) for p in os.listdir('bin')],
    long_description=markdown_contents,
    install_requires=['blessings', 'PyYAML'],
    url="https://github.com/davedash/wheeljack",
    author="Dave Dash",
    author_email="dd+github@davedash.com",
    packages=['wheeljack']
)

