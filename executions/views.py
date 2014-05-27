from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework import views
from django.http import HttpResponse

from . import negotiators, parsers
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser


from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# @api_view(['GET', 'POST'])
# def executions_list(request):
#     """
#     List all snippets, or create a new snippet.
#     """
#     if request.method == 'GET':
#         data = {"abc": 123}
# snippets = Snippet.objects.all()
# serializer = SnippetSerializer(snippets, many=True)
#         return Response(data)
#     if request.method == 'OPTIONS':
#         data = {"abc": 123}
# snippets = Snippet.objects.all()
# serializer = SnippetSerializer(snippets, many=True)
#         return Response({"abc": 123})


class ProductView(APIView):

    parser_classes = (parsers.JSONSchemaParser,)
    # content_negotiation_class = negotiators.IgnoreClientContentNegotiation

    def get(self, request, *args, **kwargs):
        data = {"abc": 123}
        data = [123, 456]
        return Response(data)

    def post(self, request, *args, **kwargs):
        try:
            # implicitly calls parser_classes
            request.DATA
        except ParseError:
            return Response('Invalid JSON', status=status.HTTP_400_BAD_REQUEST)
        # utils.store_the_json(request.DATA)
        return Response()

    def options(self, request, *args, **kwargs):
        data = {
            "name": "Snippet List",
            "description": "This viewset automatically provides `list`, `create`, `retrieve`,\n`update` and `destroy` actions.\n\nAdditionally we also provide an extra `highlight` action.",
            "renders": [
                "application/json",
                "text/html",
                "application/javascript",
                "multipart/form-data; boundary=BoUnDaRyStRiNg",
                "application/xml"
            ],
            "parses": [
                "application/json",
                "application/x-www-form-urlencoded",
                "multipart/form-data"
            ],
            "actions": {
                "POST": {
                    "pk": {
                        "type": "field",
                        "required": False,
                        "read_only": True
                    },
                    "title": {
                        "type": "string",
                        "required": False,
                        "read_only": False,
                        "max_length": 100
                    },
                    "code": {
                        "type": "string",
                        "required": True,
                        "read_only": False,
                        "max_length": 100000
                    },
                    "linenos": {
                        "type": "boolean",
                        "required": False,
                        "read_only": False
                    }
                }
            }
        }
        return Response(data)
