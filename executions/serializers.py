from django.forms import widgets
from rest_framework import serializers
from executions.models.execution import Execution


class ExecutionSerializer(serializers.HyperlinkedModelSerializer):
    # owner = serializers.Field()

    class Meta:
        model = Execution
        fields = ('url', 'owner',
                  'data', )
