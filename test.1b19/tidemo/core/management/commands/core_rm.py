"""Core command: delete object"""
from django.core.management.base import BaseCommand
# local
from ._util import name2model


class Command(BaseCommand):
    help = 'Remove object'

    def add_arguments(self, parser):
        parser.add_argument('model', type=str, help='Model (o|d|p)')
        parser.add_argument('id', type=int, help='object.pk')

    def handle(self, *args, **options):
        """:todo: catch not found"""
        if m := name2model.get(options['model']):
            m.objects.get(pk=options['id']).delete()
