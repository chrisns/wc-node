# coding=utf-8
""" test our workflow specs """
from SpiffWorkflow.specs import *
from SpiffWorkflow.operators import *

from WorkflowSpecs.UserInput import UserInput


# noinspection PyTypeChecker
class TestWorkflowSpec(WorkflowSpec):
    """ Test workflow spec """

    def __init__(self):
        WorkflowSpec.__init__(self)
        self.name = "my workflow"
        self.description = 'aa'
        task_a1 = UserInput(
            self, 'task_a1', args=["name", "face", "nose", "pets"])
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
