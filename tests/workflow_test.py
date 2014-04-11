import sys
sys.path.append("remotes/SpiffWorkflow")
sys.path.append("remotes/gvgen")

from SpiffWorkflow import Workflow
from SpiffWorkflow.specs import *
from WorkflowSpecs import *
from SpiffWorkflow.operators import *
from SpiffWorkflow.storage import dotVisualizer
from SpiffWorkflow.storage import JSONSerializer
from SpiffWorkflow.Task import *
# serializer = JSONSerializer()
import unittest

import json

# print("Workflow Spec Loaded");

# wf = Workflow(spec)

# tasks = wf.get_tasks(Task.READY)

# # kick off workflow, kinda redundant, we will always need to do this before doing anything else
# if(tasks[0].task_spec.name == "Start"):
#     wf.complete_task_from_id(tasks[0].id)
#     tasks = wf.get_tasks(Task.READY)

# # whatever happens tasks we have now should be ready and actionable

# # process the tasks
# def processAllTasks(wf):
#     # for task in wf.get_tasks(Task.READY):
#     #     wf.complete_task_from_id(task.id)
#     # print wf.get_tasks(Task.READY)
#     # for task in wf._get_waiting_tasks():
#     #     wf.complete_task_from_id(task.id)
#     # print wf.get_tasks(Task.WAITING)
#     wf.complete_all()
#     print " "

# processAllTasks(wf)
# processAllTasks(wf)
# processAllTasks(wf)
# for task in wf._get_waiting_tasks():
#     # print task
#     if task.task_spec.name == 'task_a1':
#         print task
#         task.set_data(**{
#                  'pets':             2,
#                  'nose':           3,
#                  'face': 'false',
#                  'name': 'hello'})
#     # wf.complete_task_from_id(task.id)
# processAllTasks(wf)

# # processAllTasks(wf)

# # processAllTasks(wf)
# # 
# # processAllTasks(wf)

# # tasks = wf.get_tasks(Task.READY)

# from SpiffWorkflow.storage import JSONSerializer

# savedJSON = wf.serialize(JSONSerializer())

# print("serialize");
# open("WorkflowTestExecution.json", "w").write(savedJSON)

# print("deserialize");
# restoredWF = JSONSerializer().deserialize_workflow(savedJSON)

# processAllTasks(restoredWF)

# restoredWF.dump();
# wf.dump()
# print("Workflow is is_completed" if wf.is_completed() else "Workflow is not yet complete")

class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.json = open('Workflow.json').read()
        self.spec = JSONSerializer().deserialize_workflow_spec(self.json)
        self.wf = Workflow(self.spec)

    def tearDown(self):
        self.json = None
        self.spec = None 
        self.wf = None

    def testValidJson(self):
        self.assertTrue(json.loads(self.json))

    def testValidSpec(self):
        print self.spec
        
        self.assertTrue(json.loads(self.json))

    def testSimpleWorkflowFlight(self):
        # check we have a start
        self.assertEqual(self.wf.get_tasks(Task.READY)[0].task_spec.name, 'Start')
        # move past the start
        self.wf.complete_all()

        # check we have our task named correctly and with the inputs we want in the workflow
        myTask = self.wf._get_waiting_tasks()[0]
        self.assertEqual(myTask.task_spec.name, 'task_a1')
        self.assertEqual(myTask.task_spec.__class__.__name__, 'UserInput')
        self.assertEqual(myTask._state, Task.WAITING)

        # try to move forwards
        self.wf.complete_all()

        # check we are still waiting on the input after trying to proceed
        myTask = self.wf._get_waiting_tasks()[0]
        self.assertEqual(myTask.task_spec.name, 'task_a1')
        self.assertEqual(myTask.task_spec.__class__.__name__, 'UserInput')
        self.assertEqual(myTask._state, Task.WAITING)
        # set some data
        dummyData = {
            'nose':  3,
            'face': 'false',
            'name': 'hello'
        }
        self.assertIsNone(myTask.set_data(**dummyData))
        self.assertEqual(myTask.get_data('nose'), 3)
        self.assertEqual(myTask.get_data('face'), 'false')
        self.assertEqual(myTask.get_data('name'), 'hello')

        self.wf.complete_all()

        # check we are still waiting on the input after trying to proceed with partial info
        myTask = self.wf._get_waiting_tasks()[0]
        self.assertEqual(myTask.task_spec.name, 'task_a1')
        self.assertEqual(myTask.task_spec.__class__.__name__, 'UserInput')
        self.assertEqual(myTask._state, Task.WAITING)

        self.assertIsNone(myTask.set_data(**{'pets' : 'ha'}))
        self.assertEqual(myTask.get_data('pets'), 'ha')
        self.wf.complete_all()

        # check that the now waiting task has moved on to the next thing in the workflow
        myTask = self.wf._get_waiting_tasks()[0]
        self.assertEqual(myTask.task_spec.name, 'task_a2')
        self.assertEqual(myTask.task_spec.__class__.__name__, 'UserInput')
        self.assertEqual(myTask._state, Task.WAITING)

        # check that the new task has inherited the data from the previous
        self.assertEqual(myTask.get_data('nose'), 3)
        self.assertEqual(myTask.get_data('face'), 'false')
        self.assertEqual(myTask.get_data('name'), 'hello')
        self.assertEqual(myTask.get_data('pets'), 'ha')
 
if __name__ == '__main__':
    unittest.main()