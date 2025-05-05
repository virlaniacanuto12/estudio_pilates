# studio/urls.py

from django.urls import path
from . import views

app_name = 'studio'

urlpatterns = [
    # Serviços
    path('', views.lista_servicos, name='lista_servicos'), 
    path('novo/', views.novo_servico, name='novo_servico'),
    path('editar/<int:pk>/', views.editar_servico, name='editar_servico'),
    path('excluir/<int:pk>/', views.excluir_servico, name='excluir_servico'),
]