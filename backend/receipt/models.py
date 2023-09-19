from django.core.validators import MinValueValidator
from django.db import models
from user.models import User


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
    )
    color = models.CharField(
        max_length=7,
    )
    slug = models.SlugField(
        max_length=200,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Теги'
        verbose_name_plural = 'Теги'


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
    )
    measurement_unit = models.CharField(
        max_length=200,
    )

    class Meta:
        verbose_name = 'Ингридиенты'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return self.name


class Receipt(models.Model):
    tags = models.ManyToManyField(
        Tag,
        through='TagReceipt'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientReceipt',
        related_name='r_ingridient'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='r_user'
    )
    name = models.CharField(
        max_length=200
    )
    image = models.ImageField(
        upload_to='receipt/',
        null=True,
        blank=True
    )
    text = models.TextField()
    cooking_time = models.PositiveIntegerField(
        validators=(MinValueValidator(1),),
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Рецепты'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date']


class TagReceipt(models.Model):
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE
    )
    receipt = models.ForeignKey(
        Receipt,
        on_delete=models.CASCADE,
        related_name='t_receipt',
    )

    def __str__(self):
        return f'{self.tag} - {self.receipt}'

    class Meta:
        verbose_name = 'Теги рецептев'
        verbose_name_plural = 'Теги рецептев'


class IngredientReceipt(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ir_ingridient',
        verbose_name='Ингридиент'
    )
    receipt = models.ForeignKey(
        Receipt,
        on_delete=models.CASCADE,
        related_name='ir_receipt'
    )
    amount = models.PositiveIntegerField(
        validators=(MinValueValidator(1),),
        verbose_name='кол-во'
    )

    def __str__(self):
        return f'{self.receipt} - {self.ingredient} '

    class Meta:
        verbose_name = 'Игридиенты рецептев'
        verbose_name_plural = 'Игридиенты рецептев'


class FavoritesReceipt(models.Model):
    receipt = models.ForeignKey(
        Receipt,
        on_delete=models.CASCADE,
        related_name='rf_receipt',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='fr_user'
    )

    class Meta:
        verbose_name = 'Избранные рецепты'
        verbose_name_plural = 'Избранные рецепты'


class ShoppingList(models.Model):
    receipt = models.ForeignKey(
        Receipt,
        on_delete=models.CASCADE,
        related_name='sl_receipt'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sl_user'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
