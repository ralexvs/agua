# Generated by Django 2.2.3 on 2019-08-31 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catastro', '0004_auto_20190831_1103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catastro',
            name='alcantarillado',
            field=models.BooleanField(default=False, verbose_name='Paga alcantarillado'),
        ),
        migrations.AlterField(
            model_name='catastro',
            name='derecho_conexion',
            field=models.BooleanField(default=False, verbose_name='Paga conexión'),
        ),
    ]
