from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
    )
    first_name = models.CharField(
        max_length=150,
    )
    last_name = models.CharField(
        max_length=150,
    )

    def __str__(self):
        return (f'username: {self.username}'
                f'- {self.first_name} {self.last_name}')


class Follow(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='is_subscribed',
                             help_text='Пользователь который подписывается',
                             verbose_name='Подписчик',
                             )

    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='is_favorited',
                               help_text='На кого подписываются',
                               verbose_name='Автор',
                               )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name='unique_follow')
        ]

    def __str__(self):
        return f'Пользователь {self.user} подписался на {self.author}'
