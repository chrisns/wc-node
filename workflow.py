#!/usr/bin/env python
# coding=utf-8
"""Workflow definition, not executed at runtime so needs to be done at build to generate json spec file"""

from SpiffWorkflow.specs import *
from WorkflowSpecs.UserInput import UserInput
from SpiffWorkflow.operators import *
from SpiffWorkflow.storage import dotVisualizer
from SpiffWorkflow.storage import JSONSerializer


class MyWorkflowSpec(WorkflowSpec):

    def __init__(self):
        WorkflowSpec.__init__(self)
        # Build one branch.
        # a1 = Simple(self, 'task_a1')
        input_1 = UserInput(
            self, 'task_a1', args=["name", "face", "nose", "pets"])
        # a1 = Evaluate(self, 'print', args=["helloworld", ["hi there"]])
        self.start.connect(input_1)

        input_2 = UserInput(self, 'task_a2', args=["sid", "mid"])
        # a2 = Execute(self, 'Ping', args=["ping", "-t", "1", "127.0.0.1"])
        input_1.connect(input_2)

        # Build another branch.
        task_b1 = Simple(self, 'task_b1')
        self.start.connect(task_b1)

        task_b2 = Simple(self, 'task_b2')
        task_b1.connect(task_b2)

        # Merge both branches (synchronized).
        synch_1 = Join(self, 'synch_1')
        input_2.connect(synch_1)
        task_b2.connect(synch_1)

        # If-condition that does not match.
        excl_choice_1 = ExclusiveChoice(self, 'excl_choice_1')
        synch_1.connect(excl_choice_1)

        task_c1 = Simple(self, 'task_c1')
        excl_choice_1.connect(task_c1)

        task_c2 = Simple(self, 'task_c2')
        cond = Equal(
            Attrib('test_attributtask_e1'), Attrib('test_attributtask_e2'))
        excl_choice_1.connect_if(cond, task_c2)

        task_c3 = Simple(self, 'task_c3')
        excl_choice_1.connect_if(cond, task_c3)

        # If-condition that matches.
        excl_choice_2 = ExclusiveChoice(self, 'excl_choice_2')
        task_c1.connect(excl_choice_2)
        task_c2.connect(excl_choice_2)
        task_c3.connect(excl_choice_2)

        task_d1 = Simple(self, 'task_d1')
        excl_choice_2.connect(task_d1)

        task_d2 = Simple(self, 'task_d2')
        excl_choice_2.connect_if(cond, task_d2)

        task_d3 = Simple(self, 'task_d3')
        cond = Equal(
            Attrib('test_attributtask_e1'), Attrib('test_attributtask_e1'))
        excl_choice_2.connect_if(cond, task_d3)

        # If-condition that does not match.
        multichoice = MultiChoice(self, 'multi_choice_1')
        task_d1.connect(multichoice)
        task_d2.connect(multichoice)
        task_d3.connect(multichoice)

        task_e1 = Simple(self, 'task_e1')
        multichoice.connect_if(cond, task_e1)

        task_e2 = Simple(self, 'task_e2')
        cond = Equal(
            Attrib('test_attributtask_e1'), Attrib('test_attributtask_e2'))
        multichoice.connect_if(cond, task_e2)

        task_e3 = Simple(self, 'task_e3')
        cond = Equal(
            Attrib('test_attributtask_e2'), Attrib('test_attributtask_e2'))
        multichoice.connect_if(cond, task_e3)

        # StructuredSynchronizingMerge
        syncmerge = Join(self, 'struct_synch_merge_1', 'multi_choice_1')
        task_e1.connect(syncmerge)
        task_e2.connect(syncmerge)
        task_e3.connect(syncmerge)

        # Implicit parallel split.
        task_f1 = Simple(self, 'task_f1')
        syncmerge.connect(task_f1)

        task_f2 = Simple(self, 'task_f2')
        syncmerge.connect(task_f2)

        task_f3 = Simple(self, 'task_f3')
        syncmerge.connect(task_f3)

        # Discriminator
        discrim_1 = Join(self,
                         'struct_discriminator_1',
                         'struct_synch_merge_1',
                         threshold=1)
        task_f1.connect(discrim_1)
        task_f2.connect(discrim_1)
        task_f3.connect(discrim_1)

        # Loop back to the first exclusive choice.
        excl_choice_3 = ExclusiveChoice(self, 'excl_choice_3')
        discrim_1.connect(excl_choice_3)
        cond = NotEqual(Attrib('excl_choice_3_reached'), Attrib('two'))
        excl_choice_3.connect_if(cond, excl_choice_1)

        # Split into 3 branches, and implicitly split twice in addition.
        multi_instance_1 = MultiInstance(self, 'multi_instance_1', times=3)
        excl_choice_3.connect(multi_instance_1)

        # Parallel tasks.
        task_g1 = Simple(self, 'task_g1')
        task_g2 = Simple(self, 'task_g2')
        multi_instance_1.connect(task_g1)
        multi_instance_1.connect(task_g2)

        # StructuredSynchronizingMerge
        syncmergtask_e2 = Join(
            self, 'struct_synch_merge_2', 'multi_instance_1')
        task_g1.connect(syncmergtask_e2)
        task_g2.connect(syncmergtask_e2)

        # Add a final task.
        last = Simple(self, 'last')
        syncmergtask_e2.connect(last)

        # Add another final task :-).
        end = Simple(self, 'End')
        last.connect(end)


WORKFLOWSPEC = MyWorkflowSpec()

print "outputting workflow to Workflow.dot"
# noinspection Restricted_Python_calls
open("Workflow.dot", "w").write(WORKFLOWSPEC.serialize(dotVisualizer()))

print "outputting workflow to Workflow.JSON"
# noinspection Restricted_Python_calls
open("Workflow.json", "w").write(WORKFLOWSPEC.serialize(JSONSerializer()))
