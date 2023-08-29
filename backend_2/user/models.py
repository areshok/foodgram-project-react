from django.db import models

# Create your models here.
from django.contrib.auth import get_user_model
User = get_user_model()


class Follow(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='followers',
                             help_text='Пользователь который подписывается',
                             verbose_name='Подписчик',
                             )

    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followings',
        help_text='На кого подписываются',
        verbose_name='Автор',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'], name='unique_follow')
        ]

    def __str__(self):
        return f'Пользователь {self.user} подписался на {self.following}'







