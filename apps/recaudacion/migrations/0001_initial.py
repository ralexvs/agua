# Generated by Django 2.2.3 on 2019-08-07 16:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catastro', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Recaudacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.BooleanField(default=True, verbose_name='Estado')),
                ('fc', models.DateTimeField(auto_now_add=True, verbose_name='Fecha creación')),
                ('fm', models.DateTimeField(auto_now=True, verbose_name='Fecha modificación')),
                ('um', models.IntegerField(blank=True, null=True, verbose_name='Usuario modifica')),
                ('fecha', models.DateField(verbose_name='Período consumo')),
                ('descripcion', models.CharField(max_length=150, verbose_name='Descripción')),
                ('pago', models.IntegerField(verbose_name='Pago')),
                ('descuento', models.IntegerField(verbose_name='Descuento')),
                ('total_consumo', models.PositiveIntegerField(blank=True, null=True, verbose_name='Consumo M3')),
                ('total_base', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Tarifa base')),
                ('total_base_reserva', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Tarifa base reserva')),
                ('total_excedente', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Total excedente')),
                ('total_consumo_maximo', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Total consumo máximo')),
                ('subtotal', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Subtotal')),
                ('total_descuento', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='T. descuento')),
                ('total_general', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Total general')),
                ('abonado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catastro.Abonado', verbose_name='Abonado')),
                ('uc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name_plural': 'Recaudaciones',
            },
        ),
    ]
