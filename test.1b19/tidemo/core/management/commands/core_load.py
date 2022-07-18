"""Core command: bulk load objects from stdin."""

import sys
from django.core.management.base import BaseCommand
# local
from ._util import name2model


def _org(m, data):
    pk = int(data[0])
    m.objects.create(pk=pk, myid=pk * 100 + 2, name=data[1])


def _dep(m, data):
    pk = int(data[0])
    m.objects.create(
        pk=pk,
        myid=pk * 100 + 3,
        name=data[1],
        org_id=int(data[2]),
        parent_id=int(data[3]) if len(data) == 4 else None
    )


def _pers(m, data):
    m.objects.create(
        username=' '.join((data[0], data[1], data[2])),
        last_name=data[0],
        first_name=data[1],
        mid_name=data[2],
        sex=not data[2].endswith('а')
    )


class Command(BaseCommand):
    help = "Load objects from stdin"

    def add_arguments(self, parser):
        parser.add_argument('model', type=str, help='Model (o|d|p)')

    def handle(self, *args, **options):
        if m := name2model.get(options['model']):
            func = {'o': _org, 'd': _dep, 'p': _pers}[options['model']]
            while line := sys.stdin.readline():
                func(m, line.strip().split())
