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
from google.appengine.ext import endpoints
# from webtest import TestApp
from google.appengine.ext import webapp
from protorpc import messages
from protorpc import message_types
from protorpc import remote

import unittest
import json
import webtest

import wc_api

class TestApiTests(unittest.TestCase):
    """do some basic functional tests on the workflow to prove our assumptions on how it works"""
    def setUp(self):
        # self.api = endpoints.api_server([wc_api.WCApi], restricted=False)
     #    app = webapp.WSGIApplication([('/', index.IndexHandler)], debug=True)
     #    print self.api.__dict__
     #    print app.get('/')
    	# # self.application = self.api.WSGIApplication([('/', index.IndexHandler)], debug=True)
     #   	# self.api = wc_api.WCApi
        tb = testbed.Testbed()
        tb.setup_env(current_version_id='testbed.version') #needed because endpoints expects a . in this value
        tb.activate()
        tb.init_all_stubs()
        self.testbed = tb
        # self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

    def tearDown(self):
        self.spec = None
        self.workflow = None
        self.testbed.deactivate()

    def test_valid_json_spec(self):
        app = endpoints.api_server([wc_api.WCApi], restricted=False)
        testapp = webtest.TestApp(app)
        msg = {"execution_id" : 12}
        resp = testapp.post_json('/_ah/spi/execution.resume', msg)
        print resp
    	# request = message_types.VoidMessage(execution_id=1)
    	# request.execution_id = 12
    	# print self.api('execution.resume', {'execution_id': 1 })
    	# response = self.api.execution_resume(self.api, {'execution_id': 1 })
    	pass

if __name__ == '__main__':
    unittest.main()
