from django.core.validators import MinValueValidator
from django.db import models
from user.models import User


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название тега',
        max_length=200,
    )
    color = models.CharField(
        verbose_name='Цвет',
        max_length=7,
    )
    slug = models.SlugField(
        verbose_name='slug',
        max_length=200,
    )

    class Meta:
        verbose_name = 'Теги'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название ингридиента',
        max_length=200,
    )
    measurement_unit = models.CharField(
        verbose_name='единица измерения',
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
        through='TagReceipt',
        verbose_name='Теги',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientReceipt',
        related_name='r_ingridient',
        verbose_name='Ингридиенты',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='r_user',
        verbose_name='Автор',
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта',
    )
    image = models.ImageField(
        upload_to='receipt/',
        null=True,
        blank=True,
        verbose_name='Картинка',
    )
    text = models.TextField(
        verbose_name='Описание рецепта',
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления',
        validators=(MinValueValidator(1),),
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        verbose_name = 'Рецепты'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date']

    def __str__(self):
        return self.name


class TagReceipt(models.Model):
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name='Тег',
    )
    receipt = models.ForeignKey(
        Receipt,
        on_delete=models.CASCADE,
        related_name='t_receipt',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Теги рецептев'
        verbose_name_plural = 'Теги рецептев'
        constraints = [
            models.UniqueConstraint(
                fields=['tag', 'receipt'], name='unique_tagreceipt')
        ]

    def __str__(self):
        return f'{self.tag} - {self.receipt}'


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
        related_name='ir_receipt',
        verbose_name='Рецепт',
    )
    amount = models.PositiveIntegerField(
        validators=(MinValueValidator(1),),
        verbose_name='кол-во'
    )

    class Meta:
        verbose_name = 'Игридиенты рецептев'
        verbose_name_plural = 'Игридиенты рецептев'
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'receipt'],
                name='unique_ingredientreceipt',
            )
        ]

    def __str__(self):
        return f'{self.receipt} - {self.ingredient} '


class FavoritesReceipt(models.Model):
    receipt = models.ForeignKey(
        Receipt,
        on_delete=models.CASCADE,
        related_name='rf_receipt',
        verbose_name='Рецепт',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='fr_user',
        verbose_name='Пользователь',
    )

    class Meta:
        verbose_name = 'Избранные рецепты'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=['receipt', 'user'], name='unique_favoritesreceipt')
        ]


class ShoppingList(models.Model):
    receipt = models.ForeignKey(
        Receipt,
        on_delete=models.CASCADE,
        related_name='sl_receipt',
        verbose_name='Рецепт',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sl_user',
        verbose_name='Пользователь',
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['receipt', 'user'], name='unique_shoppinglist')
        ]
