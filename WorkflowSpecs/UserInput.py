# -*- coding: utf-8 -*-
from __future__ import division
# Copyright (C) 2007 Samuel Abels
#
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
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA
import subprocess

from SpiffWorkflow.Task import Task
from SpiffWorkflow.exceptions import WorkflowException
from SpiffWorkflow.specs.TaskSpec import TaskSpec


class UserInput(TaskSpec):
    """

    """

    def __init__(self, parent, name, args=None, **kwargs):
        """
        Constructor.

        :type  parent: TaskSpec
        :param parent: A reference to the parent task spec.
        :type  name: str
        :param name: The name of the task spec.
        :type  args: list
        :param args: args to pass to process (first arg is the command).
        :type  kwargs: dict
        :param kwargs: kwargs to pass-through to TaskSpec initializer.
        """
        assert parent  is not None
        assert name    is not None
        TaskSpec.__init__(self, parent, name, **kwargs)
        self.args = args

    def _try_fire(self, my_task, force = False):
        # set variables
        self.data = my_task.data
        if not my_task.data:
            return False
        # print my_task.data
        # print my_task.data
        for arg in self.args:
            # print arg
            if arg not in my_task.data:
                # print arg
                return False
        # return True
        return True


    def _update_state_hook(self, my_task):
        if not self._try_fire(my_task):
            my_task.state = Task.WAITING
            return
        super(UserInput, self)._update_state_hook(my_task)

    def serialize(self, serializer):
        s_state = serializer._serialize_task_spec(self)
        s_state['args'] = self.args
        return s_state


    @classmethod
    def deserialize(cls, serializer, wf_spec, s_state, **kwargs):
        instance = cls(wf_spec, s_state['name'])

        spec = serializer._deserialize_task_spec(wf_spec,
                                                 s_state,
                                                 instance,
                                                 **kwargs)
        spec.args = s_state['args']
        return spec