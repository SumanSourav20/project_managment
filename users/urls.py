from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet, WorkspaceViewSet, TeamViewSet, RegisterView

router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet)
router.register(r'workspaces', WorkspaceViewSet)
router.register(r'teams', TeamViewSet)

urlpatterns = [
    path('', include(router.urls)),
]