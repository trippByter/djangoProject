# Generated by Django 3.2.8 on 2021-10-25 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_alter_product_price'),
        ('carts', '0008_auto_20211025_1241'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='products',
            field=models.ManyToManyField(through='carts.CartProduct', to='products.Product'),
        ),
    ]
