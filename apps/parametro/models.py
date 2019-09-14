from django.db import models
from apps.core.models import ClaseModelo

# Create your models here.

class Entidad(ClaseModelo):

    ruc = models.CharField("RUC", max_length=13, unique=True)
    descripcion = models.CharField("Nombre Comercial", max_length=150, unique=True)
    direccion = models.CharField(
        "Dirección", max_length=150, null=True,blank=True)
    telefono = models.CharField(
        "Teléfono", max_length=15, null=True, blank=True)
    celular = models.CharField("Celular", max_length=15, null=True, blank=True)
    correo = models.EmailField(
        "Correo electrónico", max_length=254, null=True, blank=True, unique=True)
    web = models.URLField("Sitio web", max_length=200, null=True, blank=True)
    logo = models.ImageField("Logotipo", upload_to='parametro/', null=True,blank=True)

    class Meta:

        verbose_name = 'Entidad'   
        verbose_name_plural = 'Entidades'
        ordering = ['descripcion']
      
    def __str__(self):

        return '{}'.format(self.descripcion)
    
    def save(self):
        
        self.descripcion = self.descripcion.upper()
        # Invoco al metodo save() del padre
        super(Entidad, self).save()


class Servicio(ClaseModelo):

    descripcion = models.CharField("Descripción", max_length=50)
    base = models.DecimalField("Tarifa base", max_digits=4, decimal_places=2, default=2.25)
    base_reserva = models.DecimalField("Tarifa base reserva", max_digits=4, decimal_places=2, default=0.55)
    base_consumo = models.IntegerField("Base consumo M3", default=11)
    consumo_maximo = models.IntegerField("Consumo máximo", default=30)
    valor_consumo_maximo = models.DecimalField("Valor consumo máximo", max_digits=5, decimal_places=2, default=20)
    administracion = models.DecimalField(
        "Gastos administrativos", max_digits=5, decimal_places=2, default=0)
    alcantarillado = models.DecimalField(
        "Alcantarillado", max_digits=5, decimal_places=2, default=0)
    derecho_conexion = models.DecimalField(
        "Derecho conexion", max_digits=5, decimal_places=2, default=400)
    derecho_conexion_nuevo_comunidad = models.DecimalField(
        "Derecho conexion nuevo comunidad", max_digits=5, decimal_places=2, default=800)

    class Meta:

        verbose_name = ("Tipo servicio")
        verbose_name_plural = ("Tipo servicios")
        ordering = ['descripcion']


    def __str__(self):

        return '{}'.format(self.descripcion)


    def save(self):

        self.derecho_conexion_nuevo_comunidad = float(
            self.derecho_conexion) * 2
        # Invoco al metodo save() del padre
        super(Servicio, self).save()


class Tarifa(ClaseModelo):

    descripcion = models.CharField("descripcion", max_length=50)
    rango_inicial = models.IntegerField("Rango Inicial", default=0)
    rango_superior = models.IntegerField("Rango Superior", default=0)
    valor_excedente = models.DecimalField("Valor por excedente", max_digits=5, decimal_places=2, default=0)

    class Meta:

        verbose_name = ("Tarifa")
        verbose_name_plural = ("Tarifas")
        ordering = ['id']
        # Unique compuesto
        #unique_together = ('servicio', 'descripcion')


    def __str__(self):

        return '{}'.format(self.descripcion)


    def save(self):

        self.descripcion = self.descripcion.upper()
        # Invoco al metodo save() del padre
        super(Tarifa, self).save()


class Multa(ClaseModelo):
    descripcion = models.CharField("Descripción", max_length=50)
    valor = models.DecimalField("Valor", max_digits=5, decimal_places=2)

    class Meta:

        verbose_name_plural = "Multas y otros valores"
        ordering = ['descripcion']

    def __str__(self):

        return self.descripcion + " | $ " + str(self.valor)



class Descuento(ClaseModelo):

    descripcion = models.CharField("Descuento", max_length=50)
    valor = models.DecimalField("Valor", max_digits=4, decimal_places=2)

    class Meta:

        verbose_name = "Descuento"
        verbose_name_plural = "Descuentos"
        ordering = ['id']

    def __str__(self):
    
        return self.descripcion + " | $ " + str(self.valor)

    

class Pago(ClaseModelo):

    descripcion = models.CharField("Forma pago", max_length=50)

    class Meta:

        verbose_name = "Forma de pago"
        verbose_name_plural = "Forma de pagos"
        ordering = ['id']

    def __str__(self):

        return '{}'.format(self.descripcion)

    
