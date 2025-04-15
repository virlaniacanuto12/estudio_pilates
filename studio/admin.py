from django.contrib import admin
from .models import Servico # Importa o nosso modelo Servico

# Register your models here.

# Registra o modelo Servico no site administrativo do Django
admin.site.register(Servico)
