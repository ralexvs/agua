# Generated by Django 2.2.3 on 2019-08-31 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catastro', '0009_auto_20190831_1211'),
    ]

    operations = [
        migrations.AddField(
            model_name='lectura',
            name='total_administracion',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Administración'),
        ),
        migrations.AddField(
            model_name='lectura',
            name='total_alcantarillado',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Alcantarillado'),
        ),
        migrations.AddField(
            model_name='lecturadetalle',
            name='administracion',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Administración'),
        ),
        migrations.AddField(
            model_name='lecturadetalle',
            name='alcantarillado',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Alcantarillado'),
        ),
        migrations.AddField(
            model_name='lecturadetalle',
            name='derecho_conexion',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Derecho conexión'),
        ),
        migrations.AddField(
            model_name='lecturadetalle',
            name='peticionario',
            field=models.CharField(blank=True, max_length=7, null=True, verbose_name='Peticionario'),
        ),
    ]
