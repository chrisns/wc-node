#!/usr/bin/env python
"""This is for asserting some principals of how we use workflow so is a good resource to refer to if you're trying to figure why things are broken"""

import sys
sys.path.append("/Applications/GoogleAppEngineLauncher.app/Contents/Resources/GoogleAppEngine-default.bundle/Contents/Resources/google_appengine")
sys.path.append("/home/new-user/Downloads/cns/google_appengine")
sys.path.append("/opt/jenkins/google_appengine")
import dev_appserver
dev_appserver.fix_sys_path()

sys.path.append("./remotes/SpiffWorkflow")
sys.path.append("./remotes/gvgen")
from models import Execution

from google.appengine.ext import testbed
from google.appengine.ext import ndb

import unittest
import json

import wc_api

class TestApi(unittest.TestCase):
    """do some basic functional tests on the workflow to prove our assumptions on how it works"""
    def setUp(self):
        self.api = WCApi()
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

    def tearDown(self):
        self.spec = None
        self.workflow = None
        self.testbed.deactivate()

    def test_valid_json_spec(self):
    	pass

if __name__ == '__main__':
    unittest.main()
