# Generated by Django 3.2.8 on 2021-10-20 18:56

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0004_alter_product_price'),
        ('carts', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Carts',
            new_name='Cart',
        ),
    ]
