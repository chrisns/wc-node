# -*- coding: utf-8 -*-
from __future__ import division
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
import pickle
from base64 import b64encode, b64decode
from SpiffWorkflow import Workflow
from SpiffWorkflow.util.impl import get_class
from SpiffWorkflow.Task import Task
from SpiffWorkflow.operators import *
from SpiffWorkflow.specs.TaskSpec import TaskSpec
from SpiffWorkflow.specs import *
from SpiffWorkflow.storage.Serializer import Serializer
from SpiffWorkflow.storage import DictionarySerializer
from SpiffWorkflow.storage.exceptions import TaskNotSupportedError
import warnings

import pprint
from tests.TestWorkflowSpec import TestWorkflowSpec

pprint.PrettyPrinter(indent=2)

class NDBSerializer(DictionarySerializer):
    def _serialize_dict(self, thedict):
        return dict(
            (k, b64encode(pickle.dumps(v, protocol=pickle.HIGHEST_PROTOCOL)))
            for k, v in thedict.items())

    def deserialize_workflow_spec(self, s_state, **kwargs):
        return TestWorkflowSpec()

    def serialize_workflow(self, workflow, **kwargs):
        assert isinstance(workflow, Workflow)
        s_state = dict()
        s_state['wf_spec'] = dict(
            name = workflow.spec.name,
            description = workflow.spec.description,
        )

        # data
        s_state['data'] = self._serialize_dict(workflow.data)

        # last_node
        value = workflow.last_task
        s_state['last_task'] = value.id if not value is None else None

        #success
        s_state['success'] = workflow.success

        #task_tree
        s_state['task_tree'] = self._serialize_task(workflow.task_tree)
        import sys
        print sys.getsizeof(pickle.dumps(s_state))
        print sys.getsizeof(str(s_state))
        pprint.pprint(s_state)
        return s_state

    def deserialize_workflow(self, s_state, **kwargs):
        wf_spec = self.deserialize_workflow_spec(s_state['wf_spec'], **kwargs)
        # wf_spec =
        workflow = Workflow(wf_spec)

        # data
        workflow.data = self._deserialize_dict(s_state['data'])

        # outer_workflow
        # workflow.outer_workflow =  find_workflow_by_id(remap_workflow_id(s_state['outer_workflow']))

        # success
        workflow.success = s_state['success']

        # workflow
        workflow.spec = wf_spec

        # task_tree
        workflow.task_tree = self._deserialize_task(workflow, s_state['task_tree'])

        # Re-connect parents
        for task in workflow.get_tasks():
            task.parent = workflow.get_task(task.parent)

        # last_task
        workflow.last_task = workflow.get_task(s_state['last_task'])

        return workflow

    def _serialize_task(self, task, skip_children=False):
        assert isinstance(task, Task)

        if isinstance(task.task_spec, SubWorkflow):
            raise TaskNotSupportedError(
                "Subworkflow tasks cannot be serialized (due to their use of" +
                " internal_data to store the subworkflow).")

        s_state = dict()

        # id
        s_state['id'] = str(task.id)

        # workflow
        # s_state['workflow'] = task.workflow.id

        # parent
        s_state['parent'] = str(task.parent.id) if not task.parent is None else None

        # children
        if not skip_children:
            s_state['children'] = [self._serialize_task(child) for child in task.children]

        # state
        s_state['state'] = task.state
        s_state['triggered'] = task.triggered

        # task_spec
        s_state['task_spec'] = task.task_spec.name

        # last_state_change
        s_state['last_state_change'] = int(task.last_state_change)

        # data
        s_state['data'] = self._serialize_dict(task.data)

        # internal_data
        # s_state['internal_data'] = task.internal_data

        return s_state

    def _deserialize_task(self, workflow, s_state):
        assert isinstance(workflow, Workflow)
        # task_spec
        task_spec = workflow.get_task_spec_from_name(s_state['task_spec'])
        task = Task(workflow, task_spec)

        # id
        task.id = s_state['id']

        # parent
        # as the task_tree might not be complete yet
        # keep the ids so they can be processed at the end
        task.parent = s_state['parent']

        # children
        task.children = [self._deserialize_task(workflow, c) for c in s_state['children']]

        # state
        task._state = s_state['state']
        task.triggered = s_state['triggered']

        # last_state_change
        task.last_state_change = s_state['last_state_change']

        # data
        task.data = self._deserialize_dict(s_state['data'])

        # internal_data
        # task.internal_data = s_state['internal_data']

        return task
