# studio/urls.py

from django.urls import path
from . import views # Garanta que esta linha está importando as views

app_name = 'studio' # Namespace definido

urlpatterns = [
    # Nova linha: Mapeia o caminho raiz do app ('/studio/') para a view listar_servicos
    # Demos o nome 'lista_servicos' a esta rota URL
    path('', views.listar_servicos, name='lista_servicos'),
]