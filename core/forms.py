# Importa el módulo de formularios de Django para crear y validar formularios HTML
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.conf import settings
from urllib.parse import urlparse

from .models import Emprendedor


class EmprendedorPasswordResetForm(PasswordResetForm):

    def clean_email(self):
        email = self.cleaned_data['email']
        if not Emprendedor.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Este correo no está registrado como emprendedor.')
        return email

    def get_users(self, email):
        # Django filtra usuarios con has_usable_password()=True, lo que excluye a los
        # emprendedores creados con password=None. Se sobreescribe para incluirlos.
        UserModel = get_user_model()
        return UserModel._default_manager.filter(
            email__iexact=email,
            is_active=True,
        )

    def save(self, *args, **kwargs):
        parsed = urlparse(settings.SITE_URL)
        kwargs.setdefault('domain_override', parsed.netloc)
        kwargs.setdefault('use_https', parsed.scheme == 'https')
        return super().save(*args, **kwargs)
