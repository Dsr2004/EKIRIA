import traceback
import sys
from django.core.management.base import BaseCommand, CommandError
from Commands.seeders import Seeders


class Command(BaseCommand):
    help = 'help text'

    def handle(self, *args, **options):
        try:
            Seeders()
            self.stdout.write(self.style.SUCCESS("Se han creado los Seeders de forma satisfactoria"))
        except ImportError as e:
           raise e