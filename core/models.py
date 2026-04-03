from django.db import models

class Emprendedor(models.Model):
    nombre = models.CharField(max_length=50)
    tipo_documento = models.CharField(max_length=2, choices=[('CC', 'Cédula de Ciudadanía'), ('CE', 'Cédula de Extranjería')])
    documento = models.CharField(max_length=15, unique=True)
    actividad_economica = models.CharField(max_length=100)
    sector = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    direccion = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre




