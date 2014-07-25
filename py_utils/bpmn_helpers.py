# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division

from __future__ import division
from SpiffWorkflow.bpmn.specs.UserTask import UserTask as UserTaskOrig
from SpiffWorkflow.bpmn.parser.BpmnParser import BpmnParser
from SpiffWorkflow.bpmn.parser.task_parsers import UserTaskParser as UserTaskParserOrig
from SpiffWorkflow.bpmn.parser.util import full_tag
from SpiffWorkflow.Task import Task


class UserTask(UserTaskOrig):
    def __init__(self, parent, name, lane=None, **kwargs):
        super(UserTask, self).__init__(parent, name, lane, **kwargs)
        self.args = None

    def _try_fire(self, my_task, force=False):
        self.data = my_task.data
        if not self.data:
            return False
        for arg in self.args:
            if arg not in my_task.data:
                return False
        return True

    def _update_state_hook(self, my_task):
        if not self._try_fire(my_task):
            my_task.state = Task.WAITING
            return
        return super(UserTask, self)._update_state_hook(my_task)


class UserTaskParser(UserTaskParserOrig):
    def parse_node(self):
        super(UserTaskParser, self).parse_node()
        self.task.args = []
        form_fields = self.xpath('.//{http://activiti.org/bpmn}formField')
        if form_fields.__len__ >= 1:
            for form_field in form_fields:
                self.task.args.append(form_field.attrib['id'])
        return self.task


class CustomBpmnParser(BpmnParser):
    OVERRIDE_PARSER_CLASSES = {
        full_tag('userTask'): (UserTaskParser, UserTask)
    }
