from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework import views
from django.http import HttpResponse

from . import negotiators, parsers
from executions.serializers import ExecutionSerializer
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
from rest_framework.generics import GenericAPIView
from django.utils.datastructures import SortedDict

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


class ProductView(views.APIView):
    serializer_class = ExecutionSerializer

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

    def metadata(self, request):
        """
        Return a dictionary of metadata about the view.
        Used to return responses for OPTIONS requests.
        """
        # By default we can't provide any form-like information, however the
        # generic views override this implementation and add additional
        # information for POST and PUT methods, based on the serializer.
        ret = super(ProductView, self).metadata(request)
        ret['actions'] = {
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
        return ret
