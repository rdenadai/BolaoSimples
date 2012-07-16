# webapp.json.serializer
from django.core import serializers

def Serialize(data, root_name=None):
    queryset = data[0]
    qtde = data[1]
    if not root_name:
        root_name = queryset.model._meta.verbose_name_plural
    return '{"total": %s, "%s": %s}' % (qtde, root_name, serializers.serialize('json', queryset, indent=2, use_natural_keys=True))