"""REST urls (actions)"""
from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'o', views.OrgViewSet)
router.register(r'd', views.DepartViewSet)
router.register(r'p', views.PersonViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
