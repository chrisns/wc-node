# -*- coding: utf-8 -*-
from __future__ import division

from SpiffWorkflow.Task import Task
from SpiffWorkflow.specs.TaskSpec import TaskSpec


# noinspection PyUnusedLocal,PyTypeChecker
class UserInput(TaskSpec):
    """ User input task spec """

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
        assert parent is not None
        assert name is not None
        TaskSpec.__init__(self, parent, name, **kwargs)
        self.args = args

    def _try_fire(self, my_task, force=False):
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

    def serialize(self, serializer, **kwargs):
        """
        serializer
        @type serializer: SpiffWorkflow.storage.DictionarySerializer.DictionarySerializer
        @param kwargs:
        @return:
        """
        s_state = serializer._serialize_task_spec(self)
        s_state['args'] = self.args
        return s_state

    @classmethod
    def deserialize(cls, serializer, wf_spec, s_state, **kwargs):
        """
        deserializer
        @param serializer:
        @param wf_spec:
        @param s_state:
        @param kwargs:
        @return:
        """
        instance = cls(wf_spec, s_state['name'])

        spec = serializer._deserialize_task_spec(wf_spec,
                                                 s_state,
                                                 instance,
                                                 **kwargs)
        spec.args = s_state['args']
        return spec
