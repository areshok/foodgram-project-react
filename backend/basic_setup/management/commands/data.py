import csv
import os
import subprocess

from django.conf import settings
from django.core.management.base import BaseCommand
from dotenv import load_dotenv
from receipt.models import Ingredient, Tag
from user.models import User

load_dotenv()

FOLDER_DATA = settings.BASE_DIR

FILES = {
    'ingredients': FOLDER_DATA / 'ingredients.csv',
    'tags': FOLDER_DATA / 'tags.csv',
}


class Command(BaseCommand):
    help = 'Первоначальная настройка'

    def handle(self, *args, **options):
        base_db()
        create_stetick()
        create_ingridients()
        create_tags()
        create_superuser()


def base_db():
    print('migrate')
    subprocess.call(['python', 'manage.py', 'migrate'])


def create_stetick():
    print('collectstatic')
    subprocess.call(['python', 'manage.py', 'collectstatic'])
    subprocess.call(
        ['cp',
         '-r',
         '/app/collected_static/.',
         '/backend_static/django_static/']
    )


def create_superuser():
    print('superuser')
    user = User.objects.create_user(
        username=os.getenv('ADMIN_USERNAME'),
        email=os.getenv('ADMIN_EMAIL'),
        password=os.getenv('ADMIN_PASSWORD'),)
    user.is_superuser = True
    user.is_staff = True
    user.save()


def create_ingridients():
    print('ingredients')
    with open(
        FILES['ingredients'],
        encoding='utf-8'
    ) as file:
        reader = csv.reader(file, delimiter=',')
        Ingredient.objects.all().delete()
        for row in reader:
            name = row[0]
            meas = row[1]
            Ingredient.objects.create(
                name=name,
                measurement_unit=meas
            )


def create_tags():
    print('tags')
    with open(FILES['tags'], encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')
        Tag.objects.all().delete()
        for row in reader:
            Tag.objects.create(**row)
