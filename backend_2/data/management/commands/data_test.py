from django.core.management.base import BaseCommand

from django.conf import settings

import os

TEST_DATA_FOLDER = settings.DATA_FOLDER / 'test_data'

class Command(BaseCommand):
    help = 'тестирование'

    def handle(self, *args, **options):
        print(settings.DATA_FOLDER)
        print(os.listdir(TEST_DATA_FOLDER))



