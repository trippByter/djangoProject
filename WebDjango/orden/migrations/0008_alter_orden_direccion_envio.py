# Generated by Django 3.2.8 on 2021-11-02 14:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DirEnvio', '0001_initial'),
        ('orden', '0007_alter_orden_direccion_envio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orden',
            name='direccion_envio',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='DirEnvio.direccionenvio'),
        ),
    ]
