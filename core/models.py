from django.db import models

class Emprendedor(models.Model):
    nombre = models.CharField('Nombre completo', max_length=50)
    tipo_documento = models.CharField('Tipo', max_length=2, choices=[('CC', 'Cédula de Ciudadanía'), ('CE', 'Cédula de Extranjería')])
    documento = models.CharField('Documento', max_length=15, unique=True)
    actividad = models.CharField('Actividad Económica', max_length=100)
    sector = models.CharField('Sector', max_length=100)
    telefono = models.CharField('Teléfono', max_length=20)
    email = models.EmailField('Correo Electrónico', unique=True)
    direccion = models.CharField('Dirección', max_length=200)

    def __str__(self):
        return self.nombre

