# Generated by Django 3.2 on 2023-09-07 02:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('receipt', '0004_shoppinglist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoppinglist',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sp_users', to=settings.AUTH_USER_MODEL),
        ),
    ]
