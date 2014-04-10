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

json = open('Workflow.json').read()

spec = JSONSerializer().deserialize_workflow_spec(json)

print("Workflow Spec Loaded");

wf = Workflow(spec)

tasks = wf.get_tasks(Task.READY)

# kick off workflow, kinda redundant, we will always need to do this before doing anything else
if(tasks[0].task_spec.name == "Start"):
    wf.complete_task_from_id(tasks[0].id)
    tasks = wf.get_tasks(Task.READY)

# whatever happens tasks we have now should be ready and actionable

# process the tasks
def processAllTasks(wf):
    for task in wf.get_tasks(Task.READY):
        wf.complete_task_from_id(task.id)
    print wf.get_tasks(Task.READY)
    print " "

processAllTasks(wf)


processAllTasks(wf)

processAllTasks(wf)

processAllTasks(wf)

processAllTasks(wf)

tasks = wf.get_tasks(Task.READY)



print(tasks)

wf.dump()
print("Workflow is is_completed" if wf.is_completed() else "Workflow is not yet complete")
