"""Core command: empty objects table"""
from django.core.management.base import BaseCommand
# local
from ._util import name2model


class Command(BaseCommand):
    help = 'Clean all objects'

    def add_arguments(self, parser):
        parser.add_argument('model', type=str, help='Model (o|d|p)')

    def handle(self, *args, **options):
        if m := name2model.get(options['model']):
            m.objects.all().delete()
