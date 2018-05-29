from django.db import models
from apps.resources.models import *

all_resources = Resource.objects.all()

for resource in all_resources:
    for key in resource._meta.get_fields():
        
        val = getattr(resource, key.name)
        if isinstance(val, unicode):
            print key.name
            new_val = ''.join([i if ord(i) < 128 else '' for i in val])
            setattr(resource, key.name, new_val)
    resource.save()