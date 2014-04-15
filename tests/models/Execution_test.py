#!/usr/bin/env python
"""Execution model test
Probably a good resource for seeing how to access a stored execution"""

import sys
sys.path.insert(0, "/Applications/GoogleAppEngineLauncher.app/Contents/Resources/GoogleAppEngine-default.bundle/Contents/Resources/google_appengine")
import dev_appserver
dev_appserver.fix_sys_path()

import unittest
from google.appengine.ext import testbed
from google.appengine.ext import ndb


from models import Execution

class ExecutionTests(unittest.TestCase):
    """Test we can store stuff in an Execution"""
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def test_requires_owner(self):
        """check that executions require a owner"""
        self.assertRaises(TypeError, Execution())

    # def test_owner_must_be_integer(self):
    #     self.assertRaises(datastore_errors.BadValueError, Execution(owner="a"))

    def test_valid_execution(self):
        """check we can make an execution"""
        execution = Execution(owner=100)
        self.assertIsInstance(execution, Execution)

    def test_can_have_a_urlsafe_key(self):
        """ check we generate urlsafe keys from executions """
        urlsafe_key = Execution(owner=100).put().urlsafe()
        self.assertIsInstance(urlsafe_key, str)
        self.assertEqual(len(urlsafe_key), 42)

    def test_execution_can_load(self):
        """ check we can load executions back """
        urlsafe_key = Execution(owner=100, test="value").put().urlsafe()
        restored_execution = ndb.Key(urlsafe=urlsafe_key).get()
        self.assertEqual(restored_execution.owner, 100)
        self.assertEqual(restored_execution.test, "value")

    def test_storage_workflow_execution(self):
        """check that we can put a workflow execution into a execution and then restore it"""
        # todo
        pass

    def test_list_executions(self):
        """ check that we can list executions belonging to a user and no other"""
        Execution(owner=100).put()
        Execution(owner=100).put()
        Execution(owner=100).put()
        Execution(owner=300).put()
        self.assertEqual(count_of_executions, 3) # todo

    def test_deleting_execution(self):
        """ check that we can make an execution and then destroy it and then no longer retrive """
        urlsafe_key = Execution(owner=100, test="value").put().urlsafe()
        ndb.Key(urlsafe=urlsafe_key).delete()
        pass


if __name__ == '__main__':
    unittest.main()

