from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class ClaseModelo(models.Model):

    estado = models.BooleanField("Estado", default=True)
    fc = models.DateTimeField("Fecha creación", auto_now_add=True)
    fm = models.DateTimeField("Fecha modificación", auto_now=True)
    uc = models.ForeignKey(User, verbose_name="Usuario", on_delete=models.CASCADE)
    um = models.IntegerField("Usuario modifica", blank=True, null=True)

    class Meta:
        abstract = True
