"""DRF [de]serializers"""
from rest_framework import serializers
from core import models


class OrgSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Org
        fields = ['url', 'pk', 'myid', 'name', 'fullname', 'vat', 'kpp', 'created_at', 'updated_at', 'depart_set']
        depth = 2


class DepartSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = models.Depart
        fields = '__all__'


class PersonSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Person
        # fields = '__all__'
        fields = ['url', 'id', 'myid', 'username', 'last_name', 'first_name', 'mid_name', 'is_active', 'ptype', 'sex',
                  'tz', 'date_joined', 'updated_at', 'email', 'phone', 'sn_ok', 'sn_ig', 'sn_tg', 'sn_wa', 'sn_vb',
                  'email_set', 'phone_set', 'snvk_set', 'snfb_set']
