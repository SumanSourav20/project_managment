from . import models
from rest_framework import generics, permissions, status, viewsets
from . import serializers
from rest_framework.response import Response
from rest_framework.decorators import action

class TenantView(generics.CreateAPIView):
    serializer_class = serializers.TenantSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        tenant = serializer.save()
        breakpoint()
        
        response = {
            "tenant": {
                "id": tenant.id,
                "name": tenant.name,
                "tenant_subdomain": tenant.schema_name,
            },
            "message": "Tenant registered successfully"
        }
          
        return Response(response, status=status.HTTP_201_CREATED)
    
class TenantViewSet(viewsets.ModelViewSet):
    queryset = models.Tenant.objects.all()
    serializer_class = serializers.TenantSerializer
    permission_classes = [permissions.AllowAny]
    
    # @action(detail=True, methods=['get'])
    # def retrive(self, request, pk=None):
    #     tenant = generics.get_object_or_404(models.Tenant, id=pk)
        
    #     print(tenant.name)
    #     serializer = serializers.TenantSerializer(tenant)
        
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    
    # @action(detail=False, methods=['get'])
    # def tenants(self, request):
    #     queryset = models.Tenant.objects.all()
    #     serializer = serializers.TenantSerializer(queryset, many=True)
        
    #     return Response(serializer.data, status=status.HTTP_200_OK)