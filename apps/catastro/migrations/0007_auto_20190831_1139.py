# Generated by Django 2.2.3 on 2019-08-31 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catastro', '0006_auto_20190831_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abonado',
            name='sexo',
            field=models.CharField(choices=[('HOM', 'Hombre'), ('MUJ', 'Mujer')], default='HOM', max_length=50, verbose_name='Sexo'),
        ),
        migrations.AlterField(
            model_name='catastro',
            name='alcantarillado',
            field=models.BooleanField(default=False, verbose_name='Alcantarillado'),
        ),
        migrations.AlterField(
            model_name='catastro',
            name='derecho_conexion',
            field=models.BooleanField(default=False, verbose_name='Derecho conexión'),
        ),
    ]