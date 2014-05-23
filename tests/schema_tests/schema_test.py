import sys
sys.path.append("remotes/jsonschema")
import jsonschema
import unittest
import wc_api


class SchemaTests(unittest.TestCase):

    """ test things to do with our input schema """

    def test_schema_load(self):
        """ check that we can resume an execution"""
        schema = wc_api.get_schema()
        jsonschema.Draft4Validator.check_schema(schema)

    def test_schema_validator_does_fail(self):
        """ check that we throw exceptions if things aren't right """
        schema = {
            "type": "objecta",
        }
        with self.assertRaises(jsonschema.exceptions.SchemaError):
            jsonschema.Draft4Validator.check_schema(schema)


if __name__ == '__main__':
    unittest.main()
