from django.db import models
from django_tenants.models import TenantMixin, DomainMixin

class Tenant(TenantMixin):
    name = models.CharField(max_length=255)
    created_on = models.DateField(auto_now_add=True)
    paid_until = models.DateField()
    on_trail = models.BooleanField()
    
class Domain(DomainMixin):
    pass