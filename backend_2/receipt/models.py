from django.db import models
from django.core.validators import MinValueValidator

from user.models import User


class Tag(models.Model):
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=7)
    slug = models.SlugField(max_length=200)


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)


class Receipt(models.Model):
    tags = models.ManyToManyField(Tag, through='TagReceipt')
    ingredients = models.ManyToManyField(Ingredient, through='IngredientReceipt')

    author = models.ForeignKey(User, on_delete=models.CASCADE,)
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='receipt/', null=True, blank=True)
    text = models.TextField()
    cooking_time = models.PositiveIntegerField(validators=(MinValueValidator(1),), )


class TagReceipt(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE)

class IngredientReceipt(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE)

