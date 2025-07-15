from django.urls import path
from . import views
from .views import (
    login_view_simples,
    home,
    AlunoListView,
    AlunoCreateView,
    AlunoUpdateView,
    AlunoDeleteView,
    EvolucoesAlunoView,
    PlanoListView,
    PlanoCreateView,
    PlanoUpdateView,
    PlanoDeleteView,
    ServicoListView,
    ServicoCreateView,
    ServicoUpdateView,
    ServicoDeleteView,
    ContaReceberListView,
    ContaReceberCreateView,
    ContaReceberUpdateView,
    ContaReceberDeleteView,
    ContaReceberDetailView,
    PagamentoListView,
    PagamentoCreateView,
    PagamentoDetailView,
    AulaListView, 
    AulaDetailView, 
    FrequenciaAulaView,
    AulaCreateView, 
    AulaUpdateView, 
    AulaCancelView,
    )
from django.urls import path, include


app_name = 'studio'

urlpatterns = [
    #Rota para a view de login
    path('', views.login_view_simples, name='login'),

    # Rota para a view da home page
    path('home/', views.home, name='home'),

    # Serviços
    path('servicos/', ServicoListView.as_view(), name='lista_servicos'),
    path('servicos/novo/', ServicoCreateView.as_view(), name='novo_servico'),
    path('servicos/editar/<int:pk>/', ServicoUpdateView.as_view(), name='editar_servico'),
    path('servicos/excluir/<int:pk>/', ServicoDeleteView.as_view(), name='excluir_servico'),

    # Funcionario
    path('funcionarios/', views.listar_funcionario, name='listar_funcionario'),
    path('funcionarios/novo/', views.cadastro_funcionario, name='cadastro_funcionario'),
    path('funcionarios/editar/<int:id>/', views.editar_funcionario, name='editar_funcionario'),
    path('funcionarios/excluir/<int:id>/', views.excluir_funcionario, name='excluir_funcionario'),
    
    # Aluno
    path('alunos/', AlunoListView.as_view(), name='listar_alunos'),
    path('alunos/novo/', AlunoCreateView.as_view(), name='cadastrar_aluno'),
    path('alunos/editar/<int:id>/', AlunoUpdateView.as_view(), name='editar_aluno'),
    path('alunos/excluir/<int:id>/', AlunoDeleteView.as_view(), name='excluir_aluno'),
    path("alunos/<int:id>/evolucoes/", EvolucoesAlunoView.as_view(), name="evolucoes_aluno"),

    # Plano
    path('planos/', PlanoListView.as_view(), name='listar_planos'),
    path('planos/novo/', PlanoCreateView.as_view(), name='cadastrar_plano'),
    path('planos/<int:codigo>/editar/', PlanoUpdateView.as_view(), name='editar_plano'),
    path('planos/<int:codigo>/excluir/', PlanoDeleteView.as_view(), name='excluir_plano'),


    # Aula
    path("aulas/", AulaListView.as_view(), name="listar_aulas"),
    path("aulas/nova/", AulaCreateView.as_view(), name="cadastro_aula"),
    path("aulas/<int:pk>/", AulaDetailView.as_view(), name="detalhes_aula"),
    path("aulas/<int:pk>/editar/", AulaUpdateView.as_view(), name="editar_aula"),
    path("aulas/<int:pk>/frequencia/", FrequenciaAulaView.as_view(), name="frequencia_aula"),
    path("aulas/cancelar/<int:codigo>/", AulaCancelView.as_view(), name="cancelar_aula"),

    #Contas a receber
    path('contas/', ContaReceberListView.as_view(), name='listar_contas'),
    path('contas/novo/', ContaReceberCreateView.as_view(), name='registrar_conta'),
    path('contas/editar/<int:pk>/', ContaReceberUpdateView.as_view(), name='editar_conta'),
    path('contas/excluir/<int:pk>/', ContaReceberDeleteView.as_view(), name='excluir_conta'),
    path('contas/<int:pk>/', ContaReceberDetailView.as_view(), name='detalhes_conta'),

    #Pagamentos
    path('pagamentos/novo/', PagamentoCreateView.as_view(), name='registrar_pagamento'),
    path('pagamentos/', PagamentoListView.as_view(), name='listar_pagamentos'),
    path('pagamentos/<int:pk>/', PagamentoDetailView.as_view(), name='detalhes_pagamento'),

    #Horarios
    path('agendamentos/horarios/novo/', views.cadastrar_horario_disponivel, name='cadastrar_horario_disponivel'),
    path('agendamentos/horarios/', views.listar_horarios, name='listar_horarios'),
    path('agendamentos/horarios/editar/<int:horario_id>/', views.editar_horario, name='editar_horario'),
    path('agendamentos/horarios/excluir/<int:horario_id>/', views.excluir_horario, name='excluir_horario'),

    #Agendamentos
    path('agendamentos/horarios/<int:horario_id>/agendar/', views.agendar_aluno, name='agendar_aluno'),
    path('agendamentos/gerenciar/', views.listar_agendamentos, name='listar_agendamentos'), 
    path('agendamentos/alterar/<int:agendamento_id>/', views.editar_agendamento, name='editar_agendamento'), 
    path('agendamentos/cancelar/<int:agendamento_id>/', views.excluir_agendamento, name='excluir_agendamento'), 
]
