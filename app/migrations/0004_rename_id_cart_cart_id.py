# Generated by Django 4.2.3 on 2023-07-22 14:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_cart_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='id',
            new_name='cart_id',
        ),
    ]
