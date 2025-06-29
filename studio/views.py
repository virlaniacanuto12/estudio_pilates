# studio/views.py

from django.forms import modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy

from .models import Servico
from .forms import ServicoForm, ServicoFilterForm
from .models import Funcionario
from .forms import FuncionarioForm
from .models import Aluno
from .forms import AlunoForm
from .models import Plano, ContaReceber, Pagamento, Aula, AulaAluno
from .forms import PlanoForm, ContaReceberForm, PagamentoForm, AulaForm, AulaAlunoFrequenciaForm
from .forms import CustomLoginForm

LISTAR_SERVICOS = 'studio:lista_servicos'
LISTAR_FUNCIONARIO = 'studio:listar_funcionario'
LISTAR_ALUNOS = 'studio:listar_alunos'
LISTAR_PLANOS = 'studio:listar_planos'
LISTAR_AULAS = 'studio:listar_aulas'
DETALHES_AULA = 'studio:detalhes_aula'
LISTAR_CONTAS = 'studio:listar_contas'
LISTAR_PAGAMENTOS = 'studio:listar_pagamentos'


# View Serviços
def lista_servicos(request):
    queryset = Servico.objects.all()
    filter_form = ServicoFilterForm(request.GET or None)

    if filter_form.is_valid():
        modalidade = filter_form.cleaned_data.get('modalidade')
        niveis = filter_form.cleaned_data.get('niveis_dificuldade')

        if modalidade:
            queryset = queryset.filter(modalidade__icontains=modalidade)

        if niveis:
            queryset = queryset.filter(niveis_dificuldade=niveis)

    queryset = queryset.order_by('modalidade')
    contexto = {
        'lista_servicos': queryset,
        'filter_form': filter_form,
    }
    return render(request, 'studio/servicos/listar_servicos.html', contexto)


def novo_servico(request):
    if request.method == 'POST':
        form = ServicoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(LISTAR_SERVICOS)
    else:
        form = ServicoForm()
    contexto = {
        'form': form,
    }
    return render(request, 'studio/servicos/cadastrar_servicos.html', contexto)


def editar_servico(request, pk):
    servico = get_object_or_404(Servico, pk=pk)
    if request.method == 'POST':
        form = ServicoForm(request.POST, instance=servico)
        if form.is_valid():
            form.save()
            return redirect(LISTAR_SERVICOS)
    else:
        form = ServicoForm(instance=servico)
    contexto = {
        'form': form,
    }
    return render(request, 'studio/servicos/cadastrar_servicos.html', contexto)


def excluir_servico(request, pk):
    servico = get_object_or_404(Servico, pk=pk)
    if request.method == 'POST':
        modalidade_servico = servico.modalidade
        servico.delete()
        messages.success(request, f'Serviço "{modalidade_servico}" excluído com sucesso.')
        return redirect(LISTAR_SERVICOS)
    else:
        return redirect(LISTAR_SERVICOS)


# View Funcionario
def cadastro_funcionario(request):
    if request.method == 'POST':
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(LISTAR_FUNCIONARIO)
    else:
        form = FuncionarioForm()
    return render(request, 'studio/funcionario/cadastro_funcionario.html', {'form': form})


def listar_funcionario(request):
    funcionario = Funcionario.objects.all()
    return render(request, 'studio/funcionario/listar_funcionario.html', {'funcionario': funcionario})


def editar_funcionario(request, id):
    funcionario = get_object_or_404(Funcionario, id=id)

    if request.method == 'POST':
        form = FuncionarioForm(request.POST, instance=funcionario)
        if form.is_valid():
            form.save()
            return redirect(LISTAR_FUNCIONARIO)
    else:
        form = FuncionarioForm(instance=funcionario)

    return render(request, 'studio/funcionario/editar_funcionario.html', {'form': form, 'funcionario': funcionario})


def excluir_funcionario(request, id):
    funcionario = get_object_or_404(Funcionario, id=id)

    if request.method == 'POST':
        funcionario.delete()
        messages.success(request, "Funcionário excluído com sucesso!")
        return redirect(LISTAR_FUNCIONARIO)
    return redirect(LISTAR_FUNCIONARIO)


# View Aluno
def listar_alunos(request):
    alunos = Aluno.objects.all()
    return render(request, 'studio/aluno/listar_alunos.html', {'alunos': alunos})


def cadastro_aluno(request):
    if request.method == 'POST':
        form = AlunoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(LISTAR_ALUNOS)
    else:
        form = AlunoForm()
    return render(request, 'studio/aluno/cadastrar_aluno.html', {'form': form})


def editar_aluno(request, id):
    aluno = get_object_or_404(Aluno, id=id)
    if request.method == 'POST':
        form = AlunoForm(request.POST, instance=aluno)
        if form.is_valid():
            form.save()
            return redirect(LISTAR_ALUNOS)
    else:
        form = AlunoForm(instance=aluno)
    return render(request, 'studio/aluno/editar_aluno.html', {'form': form})


def excluir_aluno(request, id):
    aluno = get_object_or_404(Aluno, id=id)
    aluno.delete()
    messages.success(request, "Aluno excluído com sucesso!")
    return redirect(LISTAR_ALUNOS)


# View Plano
def listar_planos(request):
    planos = Plano.objects.all()
    return render(request, 'studio/plano/listar_planos.html', {'planos': planos})


def cadastro_plano(request):
    if request.method == 'POST':
        form = PlanoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(LISTAR_PLANOS)
    else:
        form = PlanoForm()
    return render(request, 'studio/plano/cadastrar_plano.html', {'form': form})


def editar_plano(request, codigo):
    plano = get_object_or_404(Plano, codigo=codigo)
    if request.method == 'POST':
        form = PlanoForm(request.POST, instance=plano)
        if form.is_valid():
            form.save()
            return redirect(LISTAR_PLANOS)
    else:
        form = PlanoForm(instance=plano)
    return render(request, 'studio/plano/editar_plano.html', {'form': form})


def excluir_plano(request, codigo):
    plano = get_object_or_404(Plano, codigo=codigo)
    plano.delete()
    messages.success(request, "Plano excluído com sucesso!")
    return redirect(LISTAR_PLANOS)


# Views aula
def listar_aulas(request):
    aulas = Aula.objects.all()
    return render(request, 'studio/aula/listar_aulas.html', {'aulas': aulas})


def detalhes_aula(request, pk):
    aula = get_object_or_404(Aula, pk=pk)
    return render(request, 'studio/aula/detalhar_aula.html', {'aula': aula})


def frequencia_aula(request, pk):
    aula = get_object_or_404(Aula, pk=pk)

    if aula.cancelada:
        messages.error(request, 'Não é possível marcar frequência em uma aula cancelada.')
        return redirect(DETALHES_AULA, pk=aula.pk)

    AulaAlunoFormSet = modelformset_factory(
        AulaAluno,
        form=AulaAlunoFrequenciaForm,
        extra=0
    )

    queryset = AulaAluno.objects.filter(aula=aula)

    if request.method == 'POST':
        formset = AulaAlunoFormSet(request.POST, queryset=queryset)
        if formset.is_valid():
            formset.save()
            return redirect(DETALHES_AULA, pk=aula.pk)
    else:
        formset = Au
