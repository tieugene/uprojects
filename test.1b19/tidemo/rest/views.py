"""REST views"""
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from core import models
from . import serials


class OrgViewSet(viewsets.ModelViewSet):
    queryset = models.Org.objects.all().order_by('name')
    serializer_class = serials.OrgSerializer
    permission_classes = (AllowAny,)


class DepartViewSet(viewsets.ModelViewSet):
    queryset = models.Depart.objects.all().order_by('name')
    serializer_class = serials.DepartSerializer
    permission_classes = (AllowAny,)


class PersonViewSet(viewsets.ModelViewSet):
    queryset = models.Person.objects.all().order_by('id')
    serializer_class = serials.PersonSerializer
    permission_classes = (AllowAny,)
