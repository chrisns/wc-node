import sys

sys.path.append("remotes/jsonschema")
sys.path.append("/Applications/GoogleAppEngineLauncher.app/Contents/Resources/GoogleAppEngine-default.bundle/Contents/Resources/google_appengine")
sys.path.append("/home/new-user/Downloads/cns/google_appengine")
sys.path.append("/opt/jenkins/google_appengine")
import dev_appserver
dev_appserver.fix_sys_path()
from google.appengine.ext import testbed
from google.appengine.ext import ndb
from google.appengine.ext import endpoints
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
