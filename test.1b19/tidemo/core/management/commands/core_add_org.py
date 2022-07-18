"""Core command: add Org
note: myid added automatically"""
from django.core.management.base import BaseCommand
# local
from core.models import Org


class Command(BaseCommand):
    help = "Add Org"

    def add_arguments(self, parser):
        parser.add_argument('id', type=int, help='Org.pk')
        parser.add_argument('name', type=str, help='Org.name')

    def handle(self, *args, **options):
        pk = options['id']
        Org.objects.create(pk=pk, myid=pk * 100 + 2, name=options['name'])
