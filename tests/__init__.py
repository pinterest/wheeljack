import os
import shutil
import tempfile
import unittest
from wheeljack.config import _clear_cache

DUMMY_CONFIG = """
global:
    host: github.com
repos:
  wheeljack:
    source: davedash/wheeljack
  nuggets:
    source: Pinterest/nuggets
"""


class TestCase(unittest.TestCase):
    def setUp(self):
        _clear_cache()
        if '/usr/local/bin' not in os.environ['PATH']:
            os.environ['PATH'] = ':'.join((os.environ['PATH'],
                                           '/usr/local/bin'))
        self.tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)
        if 'WHEELJACK_CODE' in os.environ:
            del os.environ['WHEELJACK_CODE']
