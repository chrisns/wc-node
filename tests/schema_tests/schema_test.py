# coding=utf-8
""" test the schema """
import unittest

from SpiffWorkflow.bpmn.BpmnWorkflow import BpmnWorkflow
import jsonschema
from mock import patch

import main
from workflow import BpmnHelper


class SchemaTests(unittest.TestCase):
    """ test things to do with our input schema """

    def setUp(self):
        self.spec = BpmnHelper().load_workflow_spec('tests/TestWorkflowSpec.bpmn', 'workflow')

    def test_schema_load(self):
        """ check that we can resume an execution"""
        schema = main.get_schema()
        jsonschema.Draft4Validator.check_schema(schema)

    def test_schema_validator_does_fail(self):
        """ check that we throw exceptions if things aren't right """
        schema = {
            "type": "objecta",
        }
        # noinspection PyUnresolvedReferences
        with self.assertRaises(jsonschema.exceptions.SchemaError):
            jsonschema.Draft4Validator.check_schema(schema)

    @patch('main.get_schema')
    def test_post_execution_with_invalid_input(self, mock_get_schema):
        """ test posting to an execution with invalid input"""
        mock_get_schema.return_value = {'properties': []}
        execution = BpmnWorkflow(self.spec)
        execution.complete_all()
        with self.assertRaises(Exception) as ex:
            main.get_filtered_schema(execution)
        self.assertEqual('Unmapped input', ex.exception.message)


if __name__ == '__main__':
    unittest.main()  # pragma: no cover
