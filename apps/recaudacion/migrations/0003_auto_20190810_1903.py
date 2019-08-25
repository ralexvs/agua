# Generated by Django 2.2.3 on 2019-08-11 00:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recaudacion', '0002_recaudaciondetalle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recaudacion',
            name='descuento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parametro.Descuento', verbose_name='Descuento'),
        ),
        migrations.AlterField(
            model_name='recaudacion',
            name='pago',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parametro.Pago', verbose_name='Pago'),
        ),
    ]
