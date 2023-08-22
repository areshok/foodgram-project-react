from django.db import models

# Create your models here.

from user.models import User



# таблица тегов
class Tag(models.Model):
    name = models.TextField(max_length=200)
    color = models.CharField(max_length=7)
    slug = models.SlugField(max_length=200)

    def __str__(self):
        return self.name

# таблица ингридиентов
class Ingredient(models.Model):
    name = models.TextField()
    count = models.FloatField()
    measurement_unit = models.TextField()

    def __str__(self):
        return self.name

# таблица рецептов
class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.SET_NULL, null=True )
    tag = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True)

    image = models.ImageField()
    name = models.TextField(max_length=200)
    text = models.TextField()
    cooking_time = models.TimeField()

    def __str__(self):
        return self.name

class Buy(models.Model):
    pass

class Favorites(models.Model):
    pass