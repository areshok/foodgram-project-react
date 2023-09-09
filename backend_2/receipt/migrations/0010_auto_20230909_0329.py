# Generated by Django 3.2 on 2023-09-09 03:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('receipt', '0009_alter_ingredientreceipt_receipt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientreceipt',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ir_ingridient', to='receipt.ingredient'),
        ),
        migrations.AlterField(
            model_name='ingredientreceipt',
            name='receipt',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ir_receipt', to='receipt.receipt'),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='r_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='shoppinglist',
            name='receipt',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sl_receipt', to='receipt.receipt'),
        ),
        migrations.AlterField(
            model_name='shoppinglist',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sl_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
