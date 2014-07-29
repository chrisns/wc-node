__author__ = 'new-user'
from google.appengine.ext import testbed
import unittest

class BaseTestClass(unittest.TestCase):
    def setupTestbed(self):
        self.testbed = testbed.Testbed()
        # needed because endpoints expects a . in this value
        self.testbed.setup_env(current_version_id='testbed.version')
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_logservice_stub()
        self.testbed.init_memcache_stub()
