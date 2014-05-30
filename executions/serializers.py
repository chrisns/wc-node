from django.forms import widgets
from rest_framework import serializers
from executions.models.execution import Execution


class ExecutionSerializer(serializers.HyperlinkedModelSerializer):
    # owner = serializers.Field()
    model = None

    class Meta:
        model = None
    #     fields = ('url', 'owner',
    #               'data', )
    pk = serializers.Field()  # Note: `Field` is an untyped read-only field.
    title = serializers.CharField(required=False,
                                  max_length=100)
    code = serializers.CharField(widget=widgets.Textarea,
                                 max_length=100000)
    linenos = serializers.BooleanField(required=False)

    def metadata(self):
        return {"pk":
               {
                "type": "field",
                        "required": False,
                        "read_only": True
                }
                }
