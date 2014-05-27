from executions.models.execution import Execution
from executions.serializers import ExecutionSerializer
from rest_framework import generics
from rest_framework import permissions
from rest_framework import viewsets

from executions.permissions import IsOwnerOrReadOnly

from rest_framework.decorators import link


class ExecutionViewSet(viewsets.ModelViewSet):

    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Execution.objects.all()
    serializer_class = ExecutionSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    # @link(renderer_classes=[renderers.StaticHTMLRenderer])
    # def highlight(self, request, *args, **kwargs):
    #     snippet = self.get_object()
    #     return Response(snippet.highlighted)

    # def pre_save(self, obj):
    #     obj.owner = self.request.user
