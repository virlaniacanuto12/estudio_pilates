# studio/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Servico
from .forms import ServicoForm, ServicoFilterForm
from .models import Funcionario
from .forms import FuncionarioForm 


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
    return render(request, 'studio/servicos/lista_servicos.html', contexto)


def novo_servico(request):
    if request.method == 'POST':
        form = ServicoForm(request.POST) 
        if form.is_valid(): 
            form.save() 
            return redirect('studio:lista_servicos')
    else:
        form = ServicoForm() 
    contexto = {
        'form': form,
    }
    return render(request, 'studio/servicos/criar_servico.html', contexto)


def editar_servico(request, pk):
    servico = get_object_or_404(Servico, pk=pk)
    if request.method == 'POST':
        form = ServicoForm(request.POST, instance=servico)
        if form.is_valid():
            form.save()
            return redirect('studio:lista_servicos') #
    else:
        form = ServicoForm(instance=servico)
    contexto = {
        'form': form,
    }
    return render(request, 'studio/servicos/criar_servico.html', contexto)

def excluir_servico(request, pk):
    servico = get_object_or_404(Servico, pk=pk)
    if request.method == 'POST':
        modalidade_servico = servico.modalidade
        servico.delete()
        messages.success(request, f'Serviço "{modalidade_servico}" excluído com sucesso.') # <--- USO DA FUNÇÃO
        return redirect('studio:lista_servicos')
    else:
        return redirect('studio:lista_servicos')


# View Funcionario 
def cadastro_funcionario(request):
    if request.method == 'POST':
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_funcionarios')
    else:
        form = FuncionarioForm()
    return render(request, 'studio/funcionario/cadastro_funcionario.html', {'form': form})


def listar_funcionarios(request):
    funcionarios = Funcionario.objects.all()
    return render(request, 'studio/funcionario/listar_funcionario.html', {'funcionario': funcionario})


def editar_funcionario(request, id):
    funcionario = get_object_or_404(Funcionario, id=id)
    if request.method == 'POST':
        form = FuncionarioForm(request.POST, instance=funcionario)
        if form.is_valid():
            form.save()
            return redirect('listar_funcionario')
    else:
        form = FuncionarioForm(instance=funcionario)
    return render(request, 'studio/funcionario/funcionario_form.html', {'form': form})


def excluir_funcionario(request, id):
    funcionario = get_object_or_404(Funcionario, id=id)
    funcionario.delete()
    messages.success(request, "Funcionário excluído com sucesso!")
    return redirect('listar_funcionario')

def home(request):
    return render(request, 'studio/home.html')