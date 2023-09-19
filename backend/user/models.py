from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.db import models


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,)
    email = models.EmailField(
        max_length=254,
        unique=True,
        validators=(EmailValidator,))
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers',
        help_text='Пользователь который подписывается',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='authors',
        help_text='На кого подписываются',
        verbose_name='Автор',
    )

    class Meta:
        verbose_name = 'Подписки'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name='unique_subscription')
        ]

    def __str__(self):
        return f'Пользователь {self.user} подписался на {self.author}'
