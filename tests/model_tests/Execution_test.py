#!/usr/bin/env python
"""Execution model test
Probably a good resource for seeing how to access a stored execution"""

import sys
sys.path.append("./remotes/SpiffWorkflow")
sys.path.append("./remotes/gvgen")

import unittest
from google.appengine.ext import testbed
from google.appengine.ext import ndb


from models.Execution import Execution


class ExecutionTests(unittest.TestCase):

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

    def test_valid_execution(self):
        """check we can make an execution"""
        execution = Execution(owner=100)
        self.assertIsInstance(execution, Execution)

    def test_can_have_a_urlsafe_key(self):
        """ check we generate urlsafe keys from executions """
        urlsafe_key = Execution(owner=100).put().urlsafe()
        self.assertIsInstance(urlsafe_key, str)
        self.assertEqual(len(urlsafe_key), 34)

    def test_execution_can_load(self):
        """ check we can load executions back """
        urlsafe_key = Execution(owner=100, test="value").put().urlsafe()
        restored_execution = ndb.Key(urlsafe=urlsafe_key).get()
        self.assertEqual(restored_execution.owner, 100)
        self.assertEqual(restored_execution.test, "value")

    def test_storing_structured_set(self):
        """ check we can store and retrive a complex deep structured array """
        data = {
            "owner": 123,
            "test": "hello",
            "testagain": {
                "another level in": True,
                "and another": {
                    "also another": 12,
                    "and one more": {
                        "just for good measure", "here",
                    },
                },
            },
            "some other stuff here maybe": "to test",
        }
        urlsafe_key = Execution(owner=100, data=data).put().urlsafe()
        restored_execution = ndb.Key(urlsafe=urlsafe_key).get()
        self.assertEqual(restored_execution.data, data)

    def test_list_executions(self):
        """ check that we can list executions belonging to a user and no other"""
        Execution(owner=100).put()
        Execution(owner=100).put()
        Execution(owner=100).put()
        Execution(owner=300).put()
        self.assertEqual(Execution.query(Execution.owner == 100).count(), 3)

    def test_deleting_execution(self):
        """ check that we can make an execution and then destroy it and then no longer retrive """
        urlsafe_key = Execution(owner=100, test="value").put().urlsafe()
        ndb.Key(urlsafe=urlsafe_key).delete()
        self.assertIsNone(ndb.Key(urlsafe=urlsafe_key).get())

if __name__ == '__main__':
    unittest.main()
