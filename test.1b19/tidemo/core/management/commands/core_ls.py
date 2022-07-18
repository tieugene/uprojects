"""Core command: object list"""
from django.core.management.base import BaseCommand
# local
from ._util import name2model


class Command(BaseCommand):
    help = 'List objects'

    def add_arguments(self, parser):
        parser.add_argument('model', type=str, help='Model (o|d|p)')

    def handle(self, *args, **options):
        if m := name2model.get(options['model']):
            for item in m.objects.all().order_by('pk'):
                print(item.pk, str(item))
