from django.urls import path
from . import views

app_name = 'studio'

urlpatterns = [
    # Serviços
    path('', views.lista_servicos, name='lista_servicos'), 
    path('novo/', views.novo_servico, name='novo_servico'),
    path('editar/<int:pk>/', views.editar_servico, name='editar_servico'),
    path('excluir/<int:pk>/', views.excluir_servico, name='excluir_servico'),

    # Funcionario
    path('funcionarios/', views.listar_funcionarios, name='listar_funcionarios'),
    path('funcionarios/novo/', views.cadastro_funcionario, name='cadastro_funcionario'),
    path('funcionarios/editar/<int:id>/', views.editar_funcionario, name='editar_funcionario'),
    path('funcionarios/excluir/<int:id>/', views.excluir_funcionario, name='excluir_funcionario'),

]