from django.conf import settings
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# user profile on top of auth user, 
# settings.AUTH_USER_MODEL is the default user model (which is by default auth User)
class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, 
        related_name='profile',
    )
    phone_no = PhoneNumberField(null=True, blank=True, unique=True,)
    profile_pic = models.TextField(null=True, blank=True,)

class Workspace(models.Model):
    name = models.CharField(max_length=255)
    