"""Core command: add Person
:note:
- username, sex - auto
- password, myid - default
- departments - auto random

def __add_deps(pers):
    deps = Depart.objects
    deps_qty = deps.count()
    qty = random.randint(0, MAX_QTY)
    for _ in range(qty):
        Membership.objects.create(
            depart=deps.get(pk=random.randint(1, deps_qty)),
            person=pers
        )
# __add_deps(
"""
import random
from django.core.management.base import BaseCommand
# local
from core.models import Person

MAX_QTY = 5

random.seed()


class Command(BaseCommand):
    help = "Add Person"

    def add_arguments(self, parser):
        parser.add_argument('surname', type=str, help='Person.last_name')
        parser.add_argument('name', type=str, help='Person.first_name')
        parser.add_argument('midname', type=str, help='Person.mid_name')

    def handle(self, *args, **options):
        Person.objects.create(
            username=' '.join((options['surname'], options['name'], options['midname'])),
            last_name=options['surname'],
            first_name=options['name'],
            mid_name=options['midname'],
            sex=not options['midname'].endswith('а')
        )
