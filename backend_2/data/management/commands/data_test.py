from django.core.management.base import BaseCommand

from django.conf import settings

import os
import csv


from receipt.models import Tag, Ingredient

TEST_DATA_FOLDER = settings.DATA_FOLDER / 'test_data'

DATA_FILES = {
    'tag': 'tags.csv',
    'ingredient': 'ingredients.csv',
}

class Command(BaseCommand):
    help = 'тестирование'

    def handle(self, *args, **options):
        print(settings.DATA_FOLDER)
        print(os.listdir(TEST_DATA_FOLDER))
        load_tags()
        load_ingredient()

def load_tags():
    with open(TEST_DATA_FOLDER / DATA_FILES['tag'], encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')
        Tag.objects.all().delete()
        for row in reader:
            Tag.objects.create(**row)


def load_ingredient():
    with open(TEST_DATA_FOLDER / DATA_FILES['ingredient'], encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=',')
        Ingredient.objects.all().delete()
        for row in reader:
            Ingredient.objects.create(**row)




