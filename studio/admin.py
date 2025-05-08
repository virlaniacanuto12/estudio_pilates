from django.contrib import admin
from .models import Servico # Importa o nosso modelo Servico
from .models import Funcionario


# Register your models here.

# Registra o modelo Servico no site administrativo do Django
admin.site.register(Servico)
#admin.site.register(Funcionario)

@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'funcao', 'salario', 'is_admin')  
    search_fields = ('nome', 'cpf', 'funcao')  
    list_filter = ('funcao', 'is_admin')  
