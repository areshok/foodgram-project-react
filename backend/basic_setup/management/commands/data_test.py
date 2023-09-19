import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from dotenv import load_dotenv
from receipt.models import (Ingredient, IngredientReceipt, Receipt, Tag,
                            TagReceipt)
from user.models import User

load_dotenv()


TEST_DATA_FOLDER = settings.DATA_FOLDER / 'test_data'

DATA_FILES = {
    'tag': 'tags.csv',
    'ingredient': 'ingredients.csv',
    'receipt': 'receipt.csv',
    'tagreceipt': 'tagreceipt.csv',
    'ingredientreceipt': 'ingredientreceipt.csv',
    'users': 'users.csv'
}


class Command(BaseCommand):
    help = 'тестирование'

    def handle(self, *args, **options):
        print(settings.DATA_FOLDER)
        print(os.listdir(TEST_DATA_FOLDER))
        user_admin()
        users_load()
        load_tags()
        load_ingredient()
        load_receipt()
        load_tagreceipt()
        load_ingredientreceipt()


def user_admin():
    user = User.objects.create_user(
        username=os.getenv('ADMIN_USERNAME'),
        email=os.getenv('ADMIN_EMAIL'),
        password=os.getenv('ADMIN_PASSWORD'),)
    user.is_superuser = True
    user.is_staff = True
    user.save()


def users_load():
    with open(
        TEST_DATA_FOLDER / DATA_FILES['users'], encoding='utf-8'
    ) as file:
        reader = csv.DictReader(file, delimiter=',')
        for row in reader:
            User.objects.create_user(**row)


def load_tags():
    with open(
        TEST_DATA_FOLDER / DATA_FILES['tag'], encoding='utf-8'
    ) as file:
        reader = csv.DictReader(file, delimiter=';')
        Tag.objects.all().delete()
        for row in reader:
            Tag.objects.create(**row)


def load_ingredient():
    with open(
        TEST_DATA_FOLDER / DATA_FILES['ingredient'], encoding='utf-8'
    ) as file:
        reader = csv.DictReader(file, delimiter=',')
        Ingredient.objects.all().delete()
        for row in reader:
            Ingredient.objects.create(**row)


def load_receipt():
    user = User.objects.get(username='admin')
    with open(
        TEST_DATA_FOLDER / DATA_FILES['receipt'], encoding='utf-8'
    ) as file:
        reader = csv.DictReader(file, delimiter=';')
        Receipt.objects.all().delete()
        for row in reader:
            row['cooking_time'] = int(row['cooking_time'])
            Receipt.objects.create(author=user, **row)


def load_tagreceipt():
    with open(
        TEST_DATA_FOLDER / DATA_FILES['tagreceipt'], encoding='utf-8'
    ) as file:
        reader = csv.DictReader(file, delimiter=';')
        TagReceipt.objects.all().delete()
        for row in reader:
            row['receipt_id'] = int(row['receipt_id'])
            row['tag_id'] = int(row['tag_id'])
            TagReceipt.objects.create(**row)


def load_ingredientreceipt():
    with open(
        TEST_DATA_FOLDER / DATA_FILES['ingredientreceipt'], encoding='utf-8'
    ) as file:
        reader = csv.DictReader(file, delimiter=';')
        IngredientReceipt.objects.all().delete()
        for row in reader:
            row['receipt_id'] = int(row['receipt_id'])
            row['ingredient_id'] = int(row['ingredient_id'])
            row['amount'] = int(row['amount'])
            IngredientReceipt.objects.create(**row)
