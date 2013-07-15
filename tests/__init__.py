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
