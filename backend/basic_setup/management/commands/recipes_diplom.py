import csv
from random import choice, randint

from django.conf import settings
from django.core.management.base import BaseCommand
from dotenv import load_dotenv
from receipt.models import (Ingredient, IngredientReceipt, Receipt, Tag,
                            TagReceipt)
from user.models import User

load_dotenv()

# settings.BASE_DIR.parent
FILES = {
    'users': settings.DATA_FOLDER / 'users.csv',
    'food': settings.DATA_FOLDER / 'name_food.csv',
}


class Command(BaseCommand):
    help = 'Первоначальная настройка'

    def handle(self, *args, **options):
        create_test_user()
        create_test_recipes()


def create_test_user():
    with open(FILES['users'], encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=',')
        for row in reader:
            user = User.objects.create_user(**row)
            user.save()


def create_test_recipes():
    name_food = []
    with open(FILES['food'], encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            name_food.append(row[0])

    for _ in range(1, 50):
        id_tag = randint(1, 5)
        id_user = randint(1, 5)
        name_receipt = choice(name_food)
        user = User.objects.get(id=id_user)
        tag = Tag.objects.get(id=id_tag)
        receipt = Receipt.objects.create(
            author=user,
            name=name_receipt,
            text=name_receipt,
        )
        TagReceipt.objects.create(
            tag=tag,
            receipt=receipt,
        )
        for __ in range(1, 4):
            id_ingridient = randint(1, 2188)
            ingridient = Ingredient.objects.get(id=id_ingridient)
            IngredientReceipt.objects.create(
                ingredient=ingridient,
                receipt=receipt,
                amount=randint(1, 500)
            )
