import jsonschema
from rest_framework.exceptions import ParseError
from rest_framework.parsers import JSONParser

from . import schemas


class JSONSchemaParser(JSONParser):

    def parse(self, stream, media_type=None, parser_context=None):
        data = super(JSONSchemaParser, self).parse(stream, media_type,
                                                   parser_context)
        try:
            jsonschema.validate(data, schemas.json)
        except ValueError as error:
            raise ParseError(detail=error.message)
        else:
            return data
