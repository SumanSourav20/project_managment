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

    def get_full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def __str__(self):
        if self.get_full_name == "":
            return self.user.username
        return self.get_full_name 

#Workspace/company
class Workspace(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"
    
class Team(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    workspaces = models.ManyToManyField(Workspace)
    users = models.ManyToManyField(UserProfile)

    def __str__(self):
        return f"{self.name}"
