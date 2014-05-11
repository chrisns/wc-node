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

import unittest
import json
import webtest

import wc_api
from mock import patch, Mock

class TestApiTests(unittest.TestCase):
    """do some basic functional tests on the workflow to prove our assumptions on how it works"""
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.setup_env(current_version_id='testbed.version') #needed because endpoints expects a . in this value
        self.testbed.activate()
        self.testbed.init_all_stubs()
        app = endpoints.api_server([wc_api.WCApi], restricted=False)
        self.app = webtest.TestApp(app)

    @patch('urllib2.urlopen')
    def api(self, mock_urlopen=None, method=None, args=None, status_code=200, content_type='application/json', auth_required = False):
        """ helper to make api calls """
        if args is None: 
            args = {}
        if auth_required == True:
            args['user_id'] = 1234
            args['token'] = 'lala'
            mock = Mock()
            mock.read.side_effect = [json.dumps({'id' : 1234})]
            mock_urlopen.return_value = mock
        response = self.app.post_json('/_ah/spi/WCApi.' + method, args)
        self.assertEqual(response.headers['content-type'], content_type)
        self.assertEqual(response.status_code, status_code)
        if content_type == "application/json":
            return json.loads(response.body)
        else:
            return response.body

    def test_list_executions(self):
        """ check that we can list executions belonging to a user and no other"""
        Execution(owner=1234).put()
        Execution(owner=1234).put()
        key_to_check_is_present = Execution(owner=1234).put().urlsafe()
        key_to_check_is_not_present = Execution(owner=300).put().urlsafe()
        resp = self.api(method='execution_list', auth_required=True)
        self.assertEqual(len(resp['executions']), 3)
        self.assertNotIn({'execution_id':key_to_check_is_not_present}, resp['executions'])
        self.assertIn({'execution_id':key_to_check_is_present}, resp['executions'])

    def tearDown(self):
        self.testbed.deactivate()

    def test_valid_json_spec(self):
        """ test responses """
        # resp = self.api(method='execution_resume', args={"execution_id" : 12})
        resp ="s"
        print resp

if __name__ == '__main__':
    unittest.main()
