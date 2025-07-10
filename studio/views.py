from django.forms import modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.views.decorators.http import require_GET, require_POST, require_http_methods, require_safe
from django.db.models import Count, Sum, Q, F 
from django.db import models 
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Servico
from .forms import ServicoForm, ServicoFilterForm
from .models import Funcionario
from .forms import FuncionarioForm
from .models import Aluno
from .forms import AlunoForm
from .models import Plano, ContaReceber, Pagamento, Aula, AulaAluno, HorarioDisponivel, Agendamento
from .forms import PlanoForm, ContaReceberForm, PagamentoForm, AulaForm, AulaAlunoFrequenciaForm, HorarioDisponivelForm, AgendamentoForm
from .forms import CustomLoginForm
from datetime import date, datetime, timedelta
from django.utils import timezone

LISTAR_SERVICOS = 'studio:lista_servicos'
LISTAR_FUNCIONARIO = 'studio:listar_funcionario'
LISTAR_ALUNOS = 'studio:listar_alunos'
LISTAR_PLANOS = 'studio:listar_planos'
LISTAR_AULAS = 'studio:listar_aulas'
DETALHES_AULA = 'studio:detalhes_aula'
LISTAR_CONTAS = 'studio:listar_contas'
LISTAR_PAGAMENTOS = 'studio:listar_pagamentos'
LISTAR_HORARIOS = 'studio:listar_horarios'
LISTAR_AGENDAMENTOS = 'studio:listar_agendamentos'


#View Serviços

class ServicoListView(ListView):
    model = Servico
    template_name = 'studio/servicos/listar_servicos.html'
    context_object_name = 'lista_servicos'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().order_by('modalidade')
        self.filter_form = ServicoFilterForm(self.request.GET or None)

        if self.filter_form.is_valid():
            modalidade = self.filter_form.cleaned_data.get('modalidade')
            niveis = self.filter_form.cleaned_data.get('niveis_dificuldade')

            if modalidade:
                queryset = queryset.filter(modalidade__icontains=modalidade)

            if niveis:
                queryset = queryset.filter(niveis_dificuldade=niveis)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = self.filter_form
        return context


class ServicoCreateView(CreateView):
    model = Servico
    form_class = ServicoForm
    template_name = 'studio/servicos/cadastrar_servicos.html'
    success_url = reverse_lazy(LISTAR_SERVICOS)

    def form_valid(self, form):
        messages.success(self.request, "Serviço cadastrado com sucesso!")
        return super().form_valid(form)


class ServicoUpdateView(UpdateView):
    model = Servico
    form_class = ServicoForm
    template_name = 'studio/servicos/cadastrar_servicos.html'
    success_url = reverse_lazy(LISTAR_SERVICOS)

    def form_valid(self, form):
        messages.success(self.request, "Serviço atualizado com sucesso!")
        return super().form_valid(form)


class ServicoDeleteView(DeleteView):
    model = Servico
    template_name = 'studio/servicos/confirmar_exclusao_servico.html'
    success_url = reverse_lazy(LISTAR_SERVICOS)

    def form_valid(self, form):
        nome_servico = self.object.modalidade
        messages.success(self.request, f'Serviço "{nome_servico}" excluído com sucesso.')
        return super().form_valid(form)

# View Funcionario

@require_http_methods(["GET", "POST"])
def cadastro_funcionario(request):
    if request.method == 'POST':
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(LISTAR_FUNCIONARIO)
    else:
        form = FuncionarioForm()
    return render(request, 'studio/funcionario/cadastro_funcionario.html', {'form': form})


@require_GET
def listar_funcionario(request):
    funcionario = Funcionario.objects.all()
    return render(request, 'studio/funcionario/listar_funcionario.html', {'funcionario': funcionario})


@require_http_methods(["GET", "POST"])
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


@require_POST
def excluir_funcionario(request, id):
    funcionario = get_object_or_404(Funcionario, id=id)
    funcionario.delete()
    messages.success(request, "Funcionário excluído com sucesso!")
    return redirect(LISTAR_FUNCIONARIO)


# View Aluno

class AlunoListView(ListView):
    model = Aluno
    template_name = 'studio/aluno/listar_alunos.html'
    context_object_name = 'alunos'


class AlunoCreateView(CreateView):
    model = Aluno
    form_class = AlunoForm
    template_name = 'studio/aluno/cadastrar_aluno.html'
    success_url = reverse_lazy(LISTAR_ALUNOS)


class AlunoUpdateView(UpdateView):
    model = Aluno
    form_class = AlunoForm
    template_name = 'studio/aluno/editar_aluno.html'
    success_url = reverse_lazy(LISTAR_ALUNOS)
    pk_url_kwarg = 'id'


class AlunoDeleteView(DeleteView):
    model = Aluno
    template_name = 'studio/aluno/confirmar_exclusao_aluno.html'
    success_url = reverse_lazy(LISTAR_ALUNOS)
    pk_url_kwarg = 'id'

    def delete(self, request, *args, **kwargs):
        aluno = self.get_object()
        aluno.delete()
        messages.success(request, "Aluno excluído com sucesso!")
        return redirect(self.success_url)


def evolucoes_aluno(request, id):
    aluno = get_object_or_404(Aluno, id=id)
    
    participacoes = AulaAluno.objects.filter(
        aluno=aluno,
    ).exclude(
        evolucao_na_aula__isnull=True
    ).exclude(
        evolucao_na_aula__exact=''
    ).select_related('aula').order_by('-aula__data')  # ordenar por data da aula, mais recente primeiro
    
    evolucoes = [(p.aula, p.evolucao_na_aula) for p in participacoes]
    
    context = {
        'aluno': aluno,
        'evolucoes': evolucoes,
    }
    return render(request, 'studio/aluno/evolucoes_aluno.html', context)


# View Plano

class PlanoListView(ListView):
    model = Plano
    template_name = 'studio/plano/listar_planos.html'
    context_object_name = 'planos'


class PlanoCreateView(CreateView):
    model = Plano
    form_class = PlanoForm
    template_name = 'studio/plano/cadastrar_plano.html'
    success_url = reverse_lazy(LISTAR_PLANOS)


class PlanoUpdateView(UpdateView):
    model = Plano
    form_class = PlanoForm
    template_name = 'studio/plano/editar_plano.html'
    success_url = reverse_lazy(LISTAR_PLANOS)
    slug_field = 'codigo'
    slug_url_kwarg = 'codigo'


class PlanoDeleteView(DeleteView):
    model = Plano
    template_name = 'studio/plano/confirmar_exclusao_plano.html'
    success_url = reverse_lazy(LISTAR_PLANOS)
    slug_field = 'codigo'
    slug_url_kwarg = 'codigo'

    def delete(self, request, *args, **kwargs):
        plano = self.get_object()
        plano.delete()
        messages.success(request, "Plano excluído com sucesso!")
        return redirect(self.success_url)


# Views aula

@require_GET
def listar_aulas(request):
    data = request.GET.get('data')
    horario = request.GET.get('horario')
    aulas = Aula.objects.all()

    if data:
        aulas = aulas.filter(data=data)
        if horario:
            aulas = aulas.filter(horario=horario)
    elif horario:
        messages.warning(request, "Para filtrar por horário, você deve informar a data.")
        aulas = Aula.objects.none()

    return render(request, 'studio/aula/listar_aulas.html', {'aulas': aulas})


@require_GET
def detalhes_aula(request, pk):
    aula = get_object_or_404(Aula, pk=pk)
    participacoes = AulaAluno.objects.filter(aula=aula)
    return render(request, 'studio/aula/detalhar_aula.html', {'aula': aula, 'participacoes': participacoes})


@require_http_methods(["GET", "POST"])
def frequencia_aula(request, pk):
    aula = get_object_or_404(Aula, pk=pk)

    AulaAlunoFormSet = modelformset_factory(
        AulaAluno,
        form=AulaAlunoFrequenciaForm,
        extra=0
    )

    queryset = AulaAluno.objects.filter(aula=aula)

    if request.method == 'POST':
        formset = AulaAlunoFormSet(request.POST, queryset=queryset)
        if formset.is_valid():
            for form in formset:
                instance = form.save(commit=False)
                instance.aula = aula  # apenas por segurança
                instance.save()
            messages.success(request, "Frequência e evolução salvas com sucesso.")
            return redirect('studio:detalhes_aula', pk=aula.pk)
        else:
            for form in formset:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, error)
    else:
        formset = AulaAlunoFormSet(queryset=queryset)

    return render(request, 'studio/aula/frequencia_aula.html', {
        'aula': aula,
        'formset': formset
    })          


@require_http_methods(["GET", "POST"])
def cadastro_aula(request):
    if request.method == 'POST':
        form = AulaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Aula cadastrada com sucesso.")
            return redirect(LISTAR_AULAS)
    else:
        form = AulaForm()
    return render(request, 'studio/aula/cadastrar_aula.html', {'form': form})


@require_http_methods(["GET", "POST"])
def editar_aula(request, pk):
    aula = get_object_or_404(Aula, pk=pk)
    if aula.cancelada:
        messages.error(request, 'Não é possível editar uma aula cancelada.')
        return redirect(DETALHES_AULA, pk=aula.codigo)
    if request.method == 'POST':
        form = AulaForm(request.POST, instance=aula)
        if form.is_valid():
            form.save()
            messages.success(request, 'Aula atualizada com sucesso.')
            return redirect(DETALHES_AULA, pk=aula.codigo)
    else:
        form = AulaForm(instance=aula)
    return render(request, 'studio/aula/editar_aula.html', {'form': form, 'aula': aula})


@require_POST
def cancelar_aula(request, codigo):
    aula = get_object_or_404(Aula, codigo=codigo)
    aula.cancelada = True
    aula.save()
    messages.success(request, f'Aula {aula.codigo} foi cancelada com sucesso.')
    return redirect(LISTAR_AULAS)


# Views contas/pagamentos

@require_GET
def listar_contas(request):
    contas = ContaReceber.objects.all()
    aluno_id = request.GET.get('aluno')
    estado = request.GET.get('estado')
    inicio = request.GET.get('inicio')
    fim = request.GET.get('fim')
    if aluno_id:
        contas = contas.filter(aluno_id=aluno_id)
    if estado:
        estado = estado.lower()
        if estado == 'vencido':
            contas = contas.filter(vencimento__lt=date.today()).exclude(status='pago')
        elif estado in ['pendente', 'pago']:
            contas = contas.filter(status=estado)
    if inicio and fim:
        contas = contas.filter(vencimento__range=[inicio, fim])

    alunos = Aluno.objects.all()
    return render(request, 'studio/conta/listar_contas.html', {
        'contas': contas,
        'alunos': alunos,
    })


@require_http_methods(["GET", "POST"])
def registrar_conta(request):
    if request.method == 'POST':
        form = ContaReceberForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Conta registrada com sucesso.')
            return redirect(LISTAR_CONTAS)
    else:
        form = ContaReceberForm()

    contexto = {
        'form': form
    }
    return render(request, 'studio/conta/registrar_conta.html', contexto)


@require_http_methods(["GET", "POST"])
def editar_conta(request, pk):
    conta = get_object_or_404(ContaReceber, pk=pk)
    if conta.status.lower() == 'pago':
        messages.warning(request, 'Esta conta já foi paga e não pode mais ser editada.')
        return redirect('studio:listar_contas')
    if request.method == 'POST':
        form = ContaReceberForm(request.POST, instance=conta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Conta atualizada com sucesso.')
            return redirect(LISTAR_CONTAS)
    else:
        form = ContaReceberForm(instance=conta)

    contexto = {
        'form': form,
        'conta': conta,
    }
    return render(request, 'studio/conta/registrar_conta.html', contexto)

@require_POST
def excluir_conta(request, pk):
    conta = get_object_or_404(ContaReceber, pk=pk)
    conta.delete()
    messages.success(request, "Conta excluída com sucesso!")
    return redirect(LISTAR_CONTAS)

@require_GET
def detalhes_conta(request, pk):
    conta = get_object_or_404(ContaReceber, pk=pk)
    return render(request, 'studio/conta/detalhar_conta.html', {'conta': conta})

@require_http_methods(["GET", "POST"])
def registrar_pagamento(request):
    conta_id = request.GET.get('conta_id')
    if request.method == 'POST':
        form = PagamentoForm(request.POST)
        if form.is_valid():
            pagamento = form.save(commit=False)
            pagamento.valor = pagamento.conta.valor
            pagamento.status = 'Efetivado'
            pagamento.save()

            pagamento.conta.status = 'pago'
            pagamento.conta.save()

            messages.success(request, 'Pagamento registrado com sucesso.')
            return redirect(LISTAR_PAGAMENTOS)
    else:
        if conta_id:
            conta = get_object_or_404(ContaReceber, id=conta_id)
            hoje_str = timezone.now().date().strftime('%Y-%m-%d')
            form = PagamentoForm(initial={
                'conta': conta,
                'data_pagamento': timezone.now().date().strftime('%Y-%m-%d'),
            })
        else:
            form = PagamentoForm()

    return render(request, 'studio/pagamento/registrar_pagamento.html', {'form': form})


@require_GET
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

@require_GET
def detalhes_pagamento(request, pk):
    pagamento = get_object_or_404(Pagamento, pk=pk)
    return render(request, 'studio/pagamento/detalhar_pagamento.html', {'pagamento': pagamento})

# LoginView

class StudioLoginView(LoginView):
    template_name = 'studio/login.html'
    authentication_form = AuthenticationForm
    next_page = reverse_lazy('home')


# Views Horarios/Agendamento

@require_GET
def listar_horarios(request):
    horarios = HorarioDisponivel.objects.filter(
        data__gte=date.today()
    ).order_by('data', 'horario_inicio').select_related('servico', 'funcionario')

    context = {
        'horarios': horarios,
        'hoje': date.today(),
    }

    return render(request, 'studio/agendamento/listar_horarios.html', context)


@require_http_methods(["GET", "POST"])
def agendar_aluno(request, horario_id):
    horario = get_object_or_404(HorarioDisponivel, id=horario_id)

    if horario.esta_cheio:
        messages.error(request, 'Este horário não possui mais vagas disponíveis. Vagas esgotadas.')
        return redirect(LISTAR_HORARIOS)

    if request.method == 'POST':
        aluno_id = request.POST.get('aluno_id')
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

        return redirect(LISTAR_HORARIOS)

    alunos = Aluno.objects.all().order_by('nome')
    context = {
        'horario': horario,
        'alunos': alunos,
    }
    return render(request, 'studio/agendamento/agendar_aluno.html', context)


@require_GET
def listar_agendamentos(request):
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


@require_http_methods(["GET", "POST"])
def editar_agendamento(request, agendamento_id):
    agendamento = get_object_or_404(Agendamento, id=agendamento_id)

    if request.method == 'POST':
        form = AgendamentoForm(request.POST, instance=agendamento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Agendamento atualizado com sucesso!')
            return redirect(LISTAR_AGENDAMENTOS)
        else:
            messages.error(request, 'Erro ao atualizar agendamento. Verifique os dados e tente novamente.')
    else:
        form = AgendamentoForm(instance=agendamento)

    context = {
        'form': form,
        'agendamento': agendamento,
    }
    return render(request, 'studio/agendamento/editar_agendamento.html', context)

@require_http_methods(["GET", "POST"])
def excluir_agendamento(request, agendamento_id):
    agendamento = get_object_or_404(Agendamento, id=agendamento_id)

    if request.method == 'POST':
        motivo = request.POST.get('motivo_cancelamento', '').strip()
        if not agendamento.cancelado:
            agendamento.cancelar_agendamento(motivo=motivo)
            messages.success(
                request,
                f'Agendamento de {agendamento.aluno.nome} em {agendamento.horario_disponivel} cancelado com sucesso. A vaga foi liberada.'
            )
        else:
            messages.info(request, 'Este agendamento já estava cancelado.')
        return redirect(LISTAR_AGENDAMENTOS)

    return render(request, 'studio/agendamento/excluir_agendamento.html', {'agendamento': agendamento})

@require_http_methods(["GET", "POST"])
def cadastrar_horario_disponivel(request):
    if request.method == 'POST':
        form = HorarioDisponivelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Horário disponível cadastrado com sucesso!')
            return redirect(LISTAR_HORARIOS)
        else:
            messages.error(request, 'Erro ao cadastrar horário. Verifique os dados e tente novamente.')
    else:
        form = HorarioDisponivelForm()

    context = {
        'form': form,
    }
    return render(request, 'studio/agendamento/cadastrar_horario_disponivel.html', context)


@require_http_methods(["GET", "POST"])
def editar_horario(request, horario_id):
    horario = get_object_or_404(HorarioDisponivel, id=horario_id)

    if request.method == 'POST':
        form = HorarioDisponivelForm(request.POST, instance=horario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Horário disponível atualizado com sucesso!')
            return redirect(LISTAR_HORARIOS)
        else:
            messages.error(request, 'Erro ao atualizar horário. Verifique os dados e tente novamente.')
    else:
        form = HorarioDisponivelForm(instance=horario)

    context = {
        'form': form,
        'horario': horario,
    }
    return render(request, 'studio/agendamento/editar_horario.html', context)


@require_http_methods(["GET", "POST"])
def excluir_horario(request, horario_id):
    horario = get_object_or_404(HorarioDisponivel, id=horario_id)

    agendamentos_ativos = horario.agendamentos.filter(cancelado=False).exists()

    if request.method == 'POST':
        if agendamentos_ativos:
            messages.error(request, 'Não é possível excluir este horário porque existem agendamentos ativos vinculados a ele.')
            return redirect(LISTAR_HORARIOS)
        else:
            horario.delete()
            messages.success(request, 'Horário disponível excluído com sucesso!')
            return redirect(LISTAR_HORARIOS)

    return render(request, 'studio/agendamento/excluir_horario.html', {'horario': horario})

@require_GET
def home(request):
    
    hoje = date.today()
    agora = timezone.now()
    
    total_alunos_ativos = Aluno.objects.filter(status=True).count()
    
    aulas_com_vagas_hoje = HorarioDisponivel.objects.filter(
        data=hoje,
    ).annotate(
        agendamentos_ativos_count=Count('agendamentos', filter=Q(agendamentos__cancelado=False))
    ).filter(
        agendamentos_ativos_count__lt=models.F('capacidade_maxima')
    ).count()

    contas_a_receber_atraso_soma = ContaReceber.objects.filter(
        vencimento__lt=hoje,
        status='pendente'
    ).aggregate(Sum('valor'))['valor__sum'] or 0
    
    data_vencimento_proximo = hoje + timedelta(days=7)
    contas_a_vencer_proximo_soma = ContaReceber.objects.filter(
        vencimento__range=(hoje, data_vencimento_proximo),
        status='pendente'
    ).aggregate(Sum('valor'))['valor__sum'] or 0

    proximos_agendamentos_hoje = Agendamento.objects.filter(
        horario_disponivel__data=hoje,
        horario_disponivel__horario_inicio__gte=agora.time(),
        cancelado=False
    ).select_related('aluno', 'horario_disponivel__funcionario').order_by('horario_disponivel__horario_inicio')
    
    
    aniversariantes_mes = Aluno.objects.filter(
        data_nascimento__month=hoje.month,
        status=True 
    ).order_by('data_nascimento__day')

    aulas_confirmadas_hoje = Aula.objects.filter(
        data=hoje,
        cancelada=False
    ).count()


    context = {
        'dashboard_data': {
            'total_alunos_ativos': total_alunos_ativos,
            'aulas_com_vagas': aulas_com_vagas_hoje,
            'contas_em_atraso_valor': contas_a_receber_atraso_soma,
            'contas_a_vencer_proximo_valor': contas_a_vencer_proximo_soma,
            'aulas_confirmadas_hoje': aulas_confirmadas_hoje,
            'proximos_agendamentos': [
                {
                    'id': ag.id, # Adicionei o ID do agendamento
                    'data': ag.horario_disponivel.data.strftime('%d/%m/%Y'),
                    'hora_inicio': ag.horario_disponivel.horario_inicio.strftime('%H:%M'),
                    'servico': ag.horario_disponivel.servico.modalidade if ag.horario_disponivel.servico else 'N/A',
                    'instrutor': ag.horario_disponivel.funcionario.nome if ag.horario_disponivel.funcionario else 'N/A',
                    'aluno_nome': ag.aluno.nome,
                } for ag in proximos_agendamentos_hoje
            ],
            'aniversariantes_mes': [
                {'nome': aluno.nome, 'aniversario': aluno.data_nascimento}
                for aluno in aniversariantes_mes
            ],
        }
    }
    
    return render(request, 'studio/home.html', context)