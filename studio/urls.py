# studio/urls.py

from django.urls import path
from . import views # Garanta que esta linha está importando as views

app_name = 'studio' # Namespace definido

urlpatterns = [
    
    path('', views.listar_servicos, name='lista_servicos'),
    path('novo/', views.criar_servico, name='criar_servico'),
    path('editar/<int:pk>/', views.editar_servico, name='editar_servico'),
    path('excluir/<int:pk>/', views.excluir_servico, name='excluir_servico'),
]