from rest_framework import serializers
from django.contrib.auth.models import User, Group
from ..resources.models import Resource, ResourceType



class ResourceSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    resource_types = serializers.StringRelatedField(many=True)
    class Meta:
        model = Resource
        fields = ('resource_types', 'name',
                  'dedicated_to', 'address', 'city', 'state', 'zip_code', 'county','phone','contact_name','owner')

class ResourceTypeSerializer(serializers.ModelSerializer):
    # resources = serializers.PrimaryKeyRelatedField(queryset=Resource.objects.all(), many=True)
    # resource_set = ResourceSerializer(read_only=True, many=True)
    
    class Meta:
        model = ResourceType
        fields = ('name', 'description','resource_set')
        depth = 1


class UserSerializer(serializers.ModelSerializer):
    resources = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = User
        fields = ('id', 'username','resources')
        depth = 1