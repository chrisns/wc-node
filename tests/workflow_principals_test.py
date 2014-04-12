#!/usr/bin/env python
"""This is for asserting some principals of how we use workflow so is a good resource to refer to if you're trying to figure why things are broken"""

import sys
sys.path.append("./remotes/SpiffWorkflow")
sys.path.append("./remotes/gvgen")

from SpiffWorkflow import Workflow
from SpiffWorkflow.specs import *
from WorkflowSpecs import *
from SpiffWorkflow.operators import *
from SpiffWorkflow.storage import JSONSerializer
from SpiffWorkflow.Task import *
import unittest
import json


class TestWorkflowSpec(WorkflowSpec):
    """Test workflow to work with"""
    def __init__(self):
        WorkflowSpec.__init__(self)
        task_a1 = UserInput(self, 'task_a1', args=["name", "face", "nose", "pets"])
        self.start.connect(task_a1)
        task_a2 = UserInput(self, 'task_a2', args=["sid", "mildrid"])
        task_a1.connect(task_a2)

        excl_choice_1 = ExclusiveChoice(self, 'excl_choice_1')
        task_a2.connect(excl_choice_1)

        # default choice
        task_b1 = Simple(self, 'task_b1')
        excl_choice_1.connect(task_b1)


        # choice
        task_b2 = Simple(self, 'task_b2')
        cond = Equal(Attrib('mildrid'), "va")
        excl_choice_1.connect_if(cond, task_b2)

        # end
        end = Simple(self, 'End')
        task_b1.connect(end)
        task_b2.connect(end)




class WorkflowFunctionalTests(unittest.TestCase):
    """do some basic functional tests on the workflow to prove our assumptions on how it works"""
    def setUp(self):
        self.spec = TestWorkflowSpec()
        self.workflow = Workflow(self.spec)

    def tearDown(self):
        self.spec = None
        self.workflow = None

    def test_valid_json_spec(self):
        """test the basics of the json serializer/deserializer on the spec"""
        json_serialized_spec = self.spec.serialize(JSONSerializer())
        self.assertTrue(json.loads(json_serialized_spec))

        self.assertIn('nose', json_serialized_spec)
        self.assertIn('face', json_serialized_spec)
        self.assertIn('mildrid', json_serialized_spec)

        json_deserialized_spec = JSONSerializer().deserialize_workflow_spec(json_serialized_spec)
        self.assertTrue(json_deserialized_spec)

    def test_valid_json_workflow(self):
        """test the basics of the json serializer/deserializer on the workflow"""
        json_serialized_wf = self.workflow.serialize(JSONSerializer())
        self.assertTrue(json.loads(json_serialized_wf))

    def test_simple_workflow_flight(self):
        """test a flight through the workflow"""
        # check we have a start
        self.assertEqual(self.workflow.get_tasks(Task.READY)[0].task_spec.name, 'Start')
        # move past the start
        self.workflow.complete_all()

        # check we have our task named correctly and with the inputs we want in the workflow
        my_task = self.workflow._get_waiting_tasks()[0]
        self.assertEqual(my_task.task_spec.name, 'task_a1')
        self.assertIsInstance(my_task.task_spec, UserInput)
        self.assertEqual(my_task._state, Task.WAITING)

        # try to move forwards
        self.workflow.complete_all()

        # check we are still waiting on the input after trying to proceed
        my_task = self.workflow._get_waiting_tasks()[0]
        self.assertEqual(my_task.task_spec.name, 'task_a1')
        self.assertEqual(my_task.task_spec.args, ['name', 'face', 'nose', 'pets'])
        self.assertIsInstance(my_task.task_spec, UserInput)
        self.assertEqual(my_task._state, Task.WAITING)
        # set some data
        dummy_data = {
          'nose':  3,
          'face': 'false',
          'name': 'hello'
        }
        self.assertIsNone(my_task.set_data(**dummy_data))
        self.assertEqual(my_task.get_data('nose'), 3)
        self.assertEqual(my_task.get_data('face'), 'false')
        self.assertEqual(my_task.get_data('name'), 'hello')

        self.workflow.complete_all()

        # check we are still waiting on the input after trying to proceed with partial info
        my_task = self.workflow._get_waiting_tasks()[0]
        self.assertEqual(my_task.task_spec.name, 'task_a1')
        self.assertIsInstance(my_task.task_spec, UserInput)
        self.assertEqual(my_task._state, Task.WAITING)

        self.assertIsNone(my_task.set_data(**{'pets' : 'ha'}))
        self.assertEqual(my_task.get_data('pets'), 'ha')
        self.workflow.complete_all()

        # check that the now waiting task has moved on to the next thing in the workflow
        my_task = self.workflow._get_waiting_tasks()[0]
        self.assertEqual(my_task.task_spec.name, 'task_a2')
        self.assertIsInstance(my_task.task_spec, UserInput)
        self.assertEqual(my_task._state, Task.WAITING)

        # check that the new task has inherited the data from the previous
        self.assertEqual(my_task.get_data('nose'), 3)
        self.assertEqual(my_task.get_data('face'), 'false')
        self.assertEqual(my_task.get_data('name'), 'hello')
        self.assertEqual(my_task.get_data('pets'), 'ha')

        # check that an exclusive choice will listen to the data given above it and choose the non-default option
        self.assertEqual(self.workflow.get_tasks_from_spec_name('task_b1')[0]._state, Task.LIKELY)
        self.assertEqual(self.workflow.get_tasks_from_spec_name('task_b2')[0]._state, Task.MAYBE)
        self.assertIsNone(my_task.set_data(**{'sid' : 'ha', "mildrid" : "va"}))
        self.workflow.complete_all()
        self.assertEqual(self.workflow.get_tasks_from_spec_name('task_b2')[0]._state, Task.COMPLETED)
        self.assertEqual(self.workflow.get_tasks_from_spec_name('task_b1'), [])


        self.assertTrue(self.workflow.is_completed())

if __name__ == '__main__':
    unittest.main()
