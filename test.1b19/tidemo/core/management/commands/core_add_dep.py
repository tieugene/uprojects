"""Core command: add department
:note: myid added automatically"""
from django.core.management.base import BaseCommand
# 4. local
from core.models import Depart


class Command(BaseCommand):
    help = 'Add Deparment to Org'

    def add_arguments(self, parser):
        parser.add_argument('id', type=int, help='Dep.pk')
        parser.add_argument('name', type=str, help='Dep.name')
        parser.add_argument('org_id', type=int, help='Org.pk')
        parser.add_argument('parent_id', nargs='?', type=int, help='Dep.parent_id')

    def handle(self, *args, **options):
        pk = options['id']
        Depart.objects.create(
            pk=pk,
            myid=pk * 100 + 3,
            name=options['name'],
            org_id=options['org_id'],
            parent_id=options.get('parent_id')
        )
