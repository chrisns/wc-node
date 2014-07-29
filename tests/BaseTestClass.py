#!/usr/bin/env python
# coding=utf-8
"""
base test class with some helpers
"""

from google.appengine.ext import testbed
import unittest


class BaseTestClass(unittest.TestCase):
    def setup_testbed(self):
        self.testbed = testbed.Testbed()
        self.testbed.setup_env(current_version_id='testbed.version')
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_logservice_stub()
        self.testbed.init_memcache_stub()
