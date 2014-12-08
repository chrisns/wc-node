###
  #!/usr/bin/env python
# coding=utf-8
"""This is used to check that we can create a workflow definition based on the test bpmn schema"""

import unittest

from persistent_workflow.models.WorkflowEntities import *


class TestWorkflowEntityDefinitions(unittest.TestCase):
    def test_workflow_end_event_definition(self):
        """
        Test workflow end event definitions
        """
        # Arrange
        expected = ['CREATE CLASS WorkflowEndEvent EXTENDS WorkflowEntity;',
                    'ALTER CLASS WorkflowEndEvent STRICTMODE TRUE;']
        obj = WorkflowEndEvent()
        # Act.
        actual = obj.create()
        # Assert.
        self.assertItemsEqual(expected, actual)

    def test_workflow_definition(self):
        """
        Test workflow definitions
        """
        # Arrange
        expected = ['CREATE CLASS Workflow EXTENDS WorkflowEntity;',
                    'ALTER CLASS Workflow STRICTMODE TRUE;']
        obj = Workflow()
        # Act.
        actual = obj.create()
        # Assert.
        self.assertItemsEqual(expected, actual)

    def test_exclusive_gateway_definition(self):
        """
        Test exclusive gateway definitions
        """
        # Arrange
        expected = ['CREATE CLASS ExclusiveGateway EXTENDS WorkflowEntity;',
                    'ALTER CLASS ExclusiveGateway STRICTMODE TRUE;',
                    'CREATE PROPERTY ExclusiveGateway.id string',
                    'CREATE PROPERTY ExclusiveGateway.name string']
        obj = ExclusiveGateway()
        # Act.
        actual = obj.create()
        # Assert.
        self.assertItemsEqual(expected, actual)

    def test_user_task_definition(self):
        """
        Test user task definitions
        """
        # Arrange
        expected = ['CREATE CLASS UserTask EXTENDS WorkflowEntity;',
                    'ALTER CLASS UserTask STRICTMODE TRUE;',
                    'CREATE PROPERTY UserTask.id string',
                    'CREATE PROPERTY UserTask.name string']
        obj = UserTask()
        # Act.
        actual = obj.create()
        # Assert.
        self.assertItemsEqual(expected, actual)

    def test_script_task_definition(self):
        """
        Test script task definitions
        """
        # Arrange
        expected = ['CREATE CLASS ScriptTask EXTENDS WorkflowEntity;',
                    'ALTER CLASS ScriptTask STRICTMODE TRUE;',
                    'CREATE PROPERTY ScriptTask.id string',
                    'CREATE PROPERTY ScriptTask.script string',
                    'CREATE PROPERTY ScriptTask.name string']
        obj = ScriptTask()
        # Act.
        actual = obj.create()
        # Assert.
        self.assertItemsEqual(expected, actual)

    def test_form_field_value_definition(self):
        """
        Test form field value definitions
        """
        # Arrange
        expected = ['CREATE CLASS FormFieldValue EXTENDS WorkflowEntity;',
                    'ALTER CLASS FormFieldValue STRICTMODE TRUE;',
                    'CREATE PROPERTY FormFieldValue.id string',
                    'CREATE PROPERTY FormFieldValue.name string']
        obj = FormFieldValue()
        # Act.
        actual = obj.create()
        # Assert.
        self.assertItemsEqual(expected, actual)

    def test_form_field_definition(self):
        """
        Test form field definitions
        """
        # Arrange
        expected = ['CREATE CLASS FormField EXTENDS WorkflowEntity;',
                    'ALTER CLASS FormField STRICTMODE TRUE;',
                    'CREATE PROPERTY FormField.id string',
                    'CREATE PROPERTY FormField.label string',
                    'CREATE PROPERTY FormField.type string',
                    'CREATE PROPERTY FormField.weight short']
        obj = FormField()
        # Act.
        actual = obj.create()
        # Assert.
        self.assertItemsEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()  # pragma: no cover

###