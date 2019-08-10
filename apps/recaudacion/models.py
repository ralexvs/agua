from django.db import models
from apps.core.models import ClaseModelo
from apps.catastro.models import LecturaDetalle, Catastro, Abonado
from apps.parametro.models import Servicio, Tarifa



# Create your models here.

class Recaudacion(ClaseModelo):

    fecha = models.DateField("Período consumo")
    abonado = models.ForeignKey("catastro.Abonado", verbose_name="Abonado", on_delete=models.CASCADE)
    descripcion = models.CharField("Descripción", max_length=150)
    pago = models.IntegerField("Pago")
    descuento = models.IntegerField("Descuento")
    total_consumo = models.PositiveIntegerField("Consumo M3", null=True, blank=True)
    total_base = models.DecimalField("Tarifa base", max_digits=10, decimal_places=2, null=True, blank=True)
    total_base_reserva = models.DecimalField("Tarifa base reserva", max_digits=10, decimal_places=2, null=True, blank=True)
    total_excedente = models.DecimalField("Total excedente", max_digits=10, decimal_places=2, null=True, blank=True)
    total_consumo_maximo = models.DecimalField("Total consumo máximo", max_digits=10, decimal_places=2, null=True, blank=True)
    subtotal = models.DecimalField("Subtotal", max_digits=10, decimal_places=2, null=True, blank=True)
    total_descuento = models.DecimalField("T. descuento", max_digits=10, decimal_places=2, null=True, blank=True)
    total_general = models.DecimalField("Total general", max_digits=10, decimal_places=2, null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Recaudaciones"

    def __str__(self):
        return self.descripcion

class RecaudacionDetalle(ClaseModelo):
    
    recaudacion = models.ForeignKey("Recaudacion", verbose_name="Recaudación", on_delete=models.CASCADE)
    lectura = models.ForeignKey("catastro.LecturaDetalle", verbose_name="Lectura", on_delete=models.CASCADE)
    numero = models.IntegerField("Catastro")
    lectura_anterior = models.PositiveIntegerField("Lectura anterior")
    lectura_actual = models.PositiveIntegerField("Lectura actual")
    consumo = models.PositiveIntegerField("Consumo M3")
    base = models.DecimalField(
        "Tarifa base", max_digits=4, decimal_places=2, default=0)
    base_reserva = models.DecimalField(
        "Tarifa base reserva", max_digits=4, decimal_places=2, default=0)
    valor_consumo_maximo = models.DecimalField(
        "Valor consumo máximo", max_digits=10, decimal_places=2, default=0)
    valor_excedente = models.DecimalField("Valor por excedente", max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField("Total", max_digits=10, decimal_places=2, default=0)
    
    class Meta:
        verbose_name_plural = "Recaudaciones Detalle"

    def __str__(self):
        return int(self.recaudacion)


