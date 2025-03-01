from . import models
from rest_framework import serializers

class TenantSerializer(serializers.ModelSerializer):
    name =  serializers.CharField(max_length=255)
    paid_until = serializers.DateField()
    on_trail = serializers.BooleanField()
    
    class Meta:
        model = models.Tenant
        fields = ['id', 'schema_name', 'name', 'created_on', 'paid_until', 'on_trail']
        read_only_fields = ['id', 'created_on']
        
class DomainSerializer(serializers.ModelSerializer):
    pass