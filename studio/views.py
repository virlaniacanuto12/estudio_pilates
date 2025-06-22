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
from .models import Plano, ContaReceber, Pagamento, Aula, AulaAluno, HorarioDisponivel, Agendamento
from .forms import PlanoForm, ContaReceberForm, PagamentoForm, AulaForm, AulaAlunoFrequenciaForm, HorarioDisponivelForm, AgendamentoForm
from .forms import CustomLoginForm
from datetime import date, datetime 

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
            return redirect('studio:lista_servicos')
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
            return redirect('studio:lista_servicos') #
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
            return redirect('studio:listar_funcionario')
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
            return redirect('studio:listar_funcionario')
    else:
        form = FuncionarioForm(instance=funcionario)

    return render(request, 'studio/funcionario/editar_funcionario.html', {'form': form, 'funcionario': funcionario})


def excluir_funcionario(request, id):
    funcionario = get_object_or_404(Funcionario, id=id)

    if request.method == 'POST':
        funcionario.delete()
        messages.success(request, "Funcionário excluído com sucesso!")
        return redirect('studio:listar_funcionario')
    return redirect('studio:listar_funcionario')  

#View Aluno
def listar_alunos(request):
    alunos = Aluno.objects.all()
    return render(request, 'studio/aluno/listar_alunos.html', {'alunos': alunos})


def cadastro_aluno(request):
    if request.method == 'POST':
        form = AlunoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('studio:listar_alunos')
    else:
        form = AlunoForm()
    return render(request, 'studio/aluno/cadastrar_aluno.html', {'form': form})


def editar_aluno(request, id):
    aluno = get_object_or_404(Aluno, id=id)
    if request.method == 'POST':
        form = AlunoForm(request.POST, instance=aluno)
        if form.is_valid():
            form.save()
            return redirect('studio:listar_alunos')
    else:
        form = AlunoForm(instance=aluno)
    return render(request, 'studio/aluno/editar_aluno.html', {'form': form})


def excluir_aluno(request, id):
    aluno = get_object_or_404(Aluno, id=id)
    aluno.delete()
    messages.success(request, "Aluno excluído com sucesso!")
    return redirect('studio:listar_alunos')


#View Plano
def listar_planos(request):
    planos = Plano.objects.all()
    return render(request, 'studio/plano/listar_planos.html', {'planos': planos})


def cadastro_plano(request):
    if request.method == 'POST':
        form = PlanoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('studio:listar_planos')
    else:
        form = PlanoForm()
    return render(request, 'studio/plano/cadastrar_plano.html', {'form': form})


def editar_plano(request, codigo):
    plano = get_object_or_404(Plano, codigo=codigo)
    if request.method == 'POST':
        form = PlanoForm(request.POST, instance=plano)
        if form.is_valid():
            form.save()
            return redirect('studio:listar_planos')
    else:
        form = PlanoForm(instance=plano)
    return render(request, 'studio/plano/editar_plano.html', {'form': form})


def excluir_plano(request, codigo):
    plano = get_object_or_404(Plano, codigo=codigo)
    plano.delete()
    messages.success(request, "Plano excluído com sucesso!")
    return redirect('studio:listar_planos')


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
        return redirect('studio:detalhes_aula', pk=aula.pk)

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
            return redirect('studio:detalhes_aula', pk=aula.pk)
    else:
        formset = AulaAlunoFormSet(queryset=queryset)

    return render(request, 'studio/aula/frequencia_aula.html', {
        'aula': aula,
        'formset': formset,
    })


def cadastro_aula(request):
    if request.method == 'POST':
        form = AulaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('studio:listar_aulas')
    else:
        form = AulaForm()
    return render(request, 'studio/aula/cadastrar_aula.html', {'form': form})


def editar_aula(request, pk):
    aula = get_object_or_404(Aula, pk=pk)
    if aula.cancelada:
            messages.error(request, 'Não é possível editar uma aula cancelada.')
            return redirect('studio:detalhes_aula', pk=aula.pk)
    if request.method == 'POST':
        form = AulaForm(request.POST, instance=aula)
        if form.is_valid():
            form.save()
            messages.success(request, 'Aula atualizada com sucesso.')
            return redirect('studio:detalhes_aula', pk=aula.pk)
    else:
        form = AulaForm(instance=aula)
    return render(request, 'studio/aula/editar_aula.html', {'form': form, 'aula': aula})


def cancelar_aula(request, codigo):
    aula = get_object_or_404(Aula, codigo=codigo)
    aula.cancelada = True
    aula.save()
    messages.success(request, f'Aula {aula.codigo} foi cancelada com sucesso.')
    return redirect('studio:listar_aulas')


# Views contas/pagamentos
def listar_contas(request):
    contas = ContaReceber.objects.all()  # Pega todas as contas a receber
    aluno_id = request.GET.get('aluno')
    estado = request.GET.get('estado')  # agora é estado, não status
    inicio = request.GET.get('inicio')
    fim = request.GET.get('fim')
    if aluno_id:
        contas = contas.filter(aluno_id=aluno_id)
    if estado:
        contas = [c for c in contas if c.estado_atual.lower() == estado.lower()]
    if inicio and fim:
        contas = contas.filter(vencimento__range=[inicio, fim])
    
    alunos = Aluno.objects.all()
    return render(request, 'studio/conta/listar_contas.html', {
        'contas': contas,
        'alunos':alunos,})

def registrar_conta(request):
    if request.method == 'POST':
        form = ContaReceberForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Conta registrada com sucesso.')
            return redirect('studio:listar_contas')  # ou outro nome da view de listagem
    else:
        form = ContaReceberForm()

    contexto = {
        'form': form
    }
    return render(request, 'studio/conta/registrar_conta.html', contexto)

def editar_conta(request, pk):
    conta = get_object_or_404(ContaReceber, pk=pk)

    if request.method == 'POST':
        form = ContaReceberForm(request.POST, instance=conta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Conta atualizada com sucesso.')
            return redirect('studio:listar_contas')
    else:
        form = ContaReceberForm(instance=conta)

    contexto = {
        'form': form,
        'conta': conta,
    }
    return render(request, 'studio/conta/registrar_conta.html', contexto)

def registrar_pagamento(request):
    if request.method == 'POST':
        form = PagamentoForm(request.POST)
        if form.is_valid():
            pagamento = form.save(commit=False)
            pagamento.valor = pagamento.conta.valor  # valor vem da conta
            pagamento.status = 'Efetivado'
            pagamento.save()

            # Marca a conta como "pago"
            pagamento.conta.status = 'pago'
            pagamento.conta.save()

            messages.success(request, 'Pagamento registrado com sucesso.')
            return redirect('studio:listar_pagamentos')
    else:
        form = PagamentoForm()

    return render(request, 'studio/pagamento/registrar_pagamento.html', {'form': form})

def listar_pagamentos(request):
    pagamentos = Pagamento.objects.all()

    metodo = request.GET.get('metodo')
    data_inicial = request.GET.get('data_inicial')
    data_final = request.GET.get('data_final')
    aluno = request.GET.get('aluno')

    if metodo:
        pagamentos = pagamentos.filter(metodo_pagamento=metodo)
    if data_inicial and data_final:
        pagamentos = pagamentos.filter(data_pagamento__range=[data_inicial, data_final])
    if aluno:
        pagamentos = pagamentos.filter(conta__aluno__nome__icontains=aluno)

    return render(request, 'studio/pagamento/listar_pagamentos.html', {'pagamentos': pagamentos})

#LoginView - view pronta do Django para autenticação
class StudioLoginView(LoginView):
    template_name = 'studio/login.html'
    authentication_form = AuthenticationForm
    next_page = reverse_lazy('home')

def home(request):
    return render(request, 'studio/home.html')

# Views Horarios/Agendamento
def listar_horarios(request):
    horarios = HorarioDisponivel.objects.filter(
        data__gte=date.today()
    ).order_by('data', 'horario_inicio').select_related('servico', 'funcionario')

    context = {
        'horarios': horarios,
        'hoje': date.today(),
    }
   
    return render(request, 'studio/agendamento/listar_horarios.html', context)


def agendar_aluno(request, horario_id):
    horario = get_object_or_404(HorarioDisponivel, id=horario_id)

    # Verifica se o horário está cheio antes de tentar agendar
    if horario.esta_cheio:
        messages.error(request, 'Este horário não possui mais vagas disponíveis. Vagas esgotadas.')
        return redirect('studio:listar_horarios') 

    if request.method == 'POST':
        aluno_id = request.POST.get('aluno_id') # Pega o ID do aluno do formulário
        try:
            aluno = Aluno.objects.get(id=aluno_id) 

            
            agendamento, created = Agendamento.objects.get_or_create(
                horario_disponivel=horario,
                aluno=aluno,
                defaults={'cancelado': False} 
            )
            
            if not created and agendamento.cancelado:
                
                agendamento.reativar_agendamento()
                messages.success(request, f'Agendamento de {aluno.nome} reativado com sucesso para {horario}.')
            elif created:
                messages.success(request, f'Aluno {aluno.nome} agendado com sucesso para {horario}.')
            else:
               
                messages.info(request, f'Aluno {aluno.nome} já está agendado para {horario}.')

        except Aluno.DoesNotExist:
            messages.error(request, 'Aluno não encontrado. Por favor, selecione um aluno válido.')
        except Exception as e:
            messages.error(request, f'Erro ao agendar: {e}.')
        
        
        return redirect('studio:listar_horarios')
    
    alunos = Aluno.objects.all().order_by('nome') 
    context = {
        'horario': horario,
        'alunos': alunos,   
    }
    return render(request, 'studio/agendamento/agendar_aluno.html', context)

def listar_agendamentos(request):
    # Recupera todos os agendamentos, otimizando o acesso a HorarioDisponivel e Aluno
    agendamentos = Agendamento.objects.select_related('horario_disponivel', 'aluno').order_by(
        'horario_disponivel__data', 'horario_disponivel__horario_inicio', 'aluno__nome'
    )

    query_aluno = request.GET.get('aluno_nome', '').strip()
    if query_aluno:
        agendamentos = agendamentos.filter(aluno__nome__icontains=query_aluno)
        if not agendamentos.exists() and query_aluno:
            messages.info(request, f'Nenhum agendamento encontrado para o aluno "{query_aluno}".')

    query_data = request.GET.get('data_aula')
    if query_data:
        try:
            parsed_date = datetime.strptime(query_data, '%Y-%m-%d').date()
            agendamentos = agendamentos.filter(horario_disponivel__data=parsed_date)
        except ValueError:
            messages.error(request, 'Formato de data inválido para pesquisa. Use AAAA-MM-DD.')

    context = {
        'agendamentos': agendamentos,
        'query_aluno': query_aluno, 
        'query_data': query_data,   
    }
    return render(request, 'studio/agendamento/listar_agendamentos.html', context)

def editar_agendamento(request, agendamento_id):
    agendamento = get_object_or_404(Agendamento, id=agendamento_id) 

    if request.method == 'POST':
        form = AgendamentoForm(request.POST, instance=agendamento) 
        if form.is_valid():
            form.save() 
            messages.success(request, 'Agendamento atualizado com sucesso!')
            return redirect('studio:listar_agendamentos') 
        else:
            messages.error(request, 'Erro ao atualizar agendamento. Verifique os dados e tente novamente.')
    else:
        form = AgendamentoForm(instance=agendamento) 

    context = {
        'form': form,
        'agendamento': agendamento,
    }
    return render(request, 'studio/agendamento/editar_agendamento.html', context)

def excluir_agendamento(request, agendamento_id):
    agendamento = get_object_or_404(Agendamento, id=agendamento_id)

    if request.method == 'POST':
        motivo = request.POST.get('motivo_cancelamento', '').strip()

        if not agendamento.cancelado:
            agendamento.cancelar_agendamento(motivo=motivo) 
            messages.success(request, f'Agendamento de {agendamento.aluno.nome} em {agendamento.horario_disponivel} cancelado com sucesso. A vaga foi liberada.')
        else:
            messages.info(request, 'Este agendamento já estava cancelado.')

        return redirect('studio:listar_agendamentos')
    
    context = {
        'agendamento': agendamento,
    }
    return render(request, 'studio/agendamento/excluir_agendamento.html', context)

def cadastrar_horario_disponivel(request):
    if request.method == 'POST':
        form = HorarioDisponivelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Horário disponível cadastrado com sucesso!')
            
            return redirect('studio:listar_horarios') 
        else:
            
            messages.error(request, 'Erro ao cadastrar horário. Verifique os dados e tente novamente.')
    else:
        form = HorarioDisponivelForm() 

    context = {
        'form': form,
    }
    return render(request, 'studio/agendamento/cadastrar_horario_disponivel.html', context)

def editar_horario(request, horario_id):
    horario = get_object_or_404(HorarioDisponivel, id=horario_id)
    if request.method == 'POST':
        form = HorarioDisponivelForm(request.POST, instance=horario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Horário disponível atualizado com sucesso!')
            return redirect('studio:listar_horarios')
        else:
            messages.error(request, 'Erro ao atualizar horário. Verifique os dados.')
    else:
        form = HorarioDisponivelForm(instance=horario)

    context = {
        'form': form,
        'horario': horario,
    }
    return render(request, 'studio/agendamento/editar_horario.html', context)


def excluir_horario(request, horario_id):
    horario = get_object_or_404(HorarioDisponivel, id=horario_id)
    if request.method == 'POST':
        if horario.agendamentos.filter(cancelado=False).exists():
            messages.error(request, 'Não é possível excluir este horário. Existem agendamentos ativos vinculados a ele.')
            return redirect('studio:listar_horarios') 

        horario.delete()
        messages.success(request, 'Horário disponível excluído com sucesso!')
        return redirect('studio:listar_horarios')
    
    context = {
        'horario': horario,
    }
    return render(request, 'studio/agendamento/excluir_horario.html', context)


