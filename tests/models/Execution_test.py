#!/usr/bin/env python
"""Execution model test"""
"""Probably a good resource for seeing how to access a stored execution"""

import unittest
from models import Execution


class ExecutionTests(unittest.TestCase):
    """Test we can store stuff in an Execution"""
    def setUp(self):
        app_id = '_'
        datastore_file = '/dev/null'
        from google.appengine.api import apiproxy_stub_map,datastore_file_stub
        apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap() 
        stub = datastore_file_stub.DatastoreFileStub(app_id, datastore_file, '/')
        apiproxy_stub_map.apiproxy.RegisterStub('datastore_v3', stub)
        
        self.execution = Execution(owner=100)

    def tearDown(self):
        self.execution = None

    def test_execution_exists(self):
        self.assertIsInstance(self.execution, Execution)

    def test_execution_has_key(self):
        self.execution.put()
        print self.execution.__dict__
        # self.execution._validate()
        print self.execution.key
        self.assertIsInstance(self.execution, Execution)
        

if __name__ == '__main__':
    unittest.main()
