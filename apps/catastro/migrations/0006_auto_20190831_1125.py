# Generated by Django 2.2.3 on 2019-08-31 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catastro', '0005_auto_20190831_1105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catastro',
            name='peticionario',
            field=models.CharField(choices=[('NEW', 'Nuevo'), ('ANT', 'Antiguo'), ('NEW_COM', 'Nuevo en la comunidad')], default='ANT', max_length=50, verbose_name='Peticionario'),
        ),
    ]