# Importa los modelos base de Django para definir tablas de la base de datos
from django.db import models
# Importa post_save, la señal que se dispara automáticamente después de guardar un registro
from django.db.models.signals import post_save
# Importa receiver, el decorador que conecta una función a una señal de Django
from django.dispatch import receiver
# Importa get_user_model para obtener el modelo de usuario activo del proyecto (permite modelos personalizados)
from django.contrib.auth import get_user_model


# Define el modelo Emprendedor como una tabla en la base de datos
class Emprendedor(models.Model):
    nombre = models.CharField('Nombre completo', max_length=50)
    tipo_documento = models.CharField('Tipo', max_length=2, choices=[('CC', 'Cédula de Ciudadanía'), ('CE', 'Cédula de Extranjería')])
    documento = models.CharField('Documento', max_length=15, unique=True)
    actividad = models.CharField('Actividad Económica', max_length=100)
    sector = models.CharField('Sector', max_length=100)
    telefono = models.CharField('Teléfono', max_length=20)
    # El email es único porque también se usa como nombre de usuario en el sistema de autenticación
    email = models.EmailField('Correo Electrónico', unique=True)
    direccion = models.CharField('Dirección', max_length=200)

    def __str__(self):
        return self.nombre


# Escucha la señal post_save del modelo Emprendedor: se ejecuta cada vez que se guarda un Emprendedor
@receiver(post_save, sender=Emprendedor)
# Función que crea automáticamente una cuenta de usuario Django al registrar un nuevo Emprendedor
def crear_usuario_emprendedor(sender, instance, created, **kwargs):
    # Solo actúa cuando el Emprendedor es nuevo (created=True); ignora actualizaciones posteriores
    if created:
        # Obtiene la clase de usuario configurada en AUTH_USER_MODEL (por defecto django.contrib.auth.User)
        User = get_user_model()
        try:
            # Busca si ya existe un usuario con el mismo correo (sin distinguir mayúsculas) para evitar duplicados
            User.objects.get(email__iexact=instance.email)
        except User.DoesNotExist:
            # Si no existe, crea la cuenta de usuario usando el correo como nombre de usuario
            User.objects.create_user(
                # El username es el correo del emprendedor, lo que permite identificarlo unívocamente
                username=instance.email,
                # Almacena también el campo email en el perfil de usuario de Django
                email=instance.email,
                # La contraseña se deja en None (inutilizable) porque el acceso se gestiona por restablecimiento de contraseña
                password=None,
            )
