"""Core command: Object's info"""
from django.core.management.base import BaseCommand
# local
from ._util import name2model


def _org(item):
    print(
        f"Pk: {item.pk}\n"
        f"Name: {item.name}"
    )


def _dep(item):
    print(
        f"Pk: {item.pk}\n"
        f"Name: {item.name}\n"
        f"Org: {item.org_id}\n"
        f"Parent: {item.parent_id}"
    )


def _pers(item):
    print(
        f"Pk: {item.pk}\n"
        f"Last Name: {item.last_name}\n"
        f"First Name: {item.first_name}\n"
        f"Middle Name: {item.mid_name}\n"
        f"Sex: {item.sex}"
    )


class Command(BaseCommand):
    help = "Object's info"

    def add_arguments(self, parser):
        parser.add_argument('model', type=str, help='Model (o|d|p)')
        parser.add_argument('id', type=int, help='Depart.pk')

    def handle(self, *args, **options):
        """:todo: catch not found"""
        if m := name2model.get(options['model']):
            item = m.objects.get(pk=options['id'])
            {'o': _org, 'd': _dep, 'p': _pers}[options['model']](item)
