# studio/forms.py
from django import forms
from .models import Servico
from .models import Funcionario
from .models import Aluno
from .models import Plano, ContaReceber, Pagamento, Aula, AulaAluno, HorarioDisponivel, Agendamento
from django.contrib.auth.forms import AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Row, Column, Submit, HTML, Field
from crispy_bootstrap5.bootstrap5 import FloatingField
from django.utils import timezone
from datetime import date, datetime


COL_MD_6 = "col-md-6"
COL_MD_6_MB_3 = "col-md-6 mb-3"


class ServicoForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = ['modalidade', 'niveis_dificuldade', 'descricao']

        widgets = {
            'modalidade': forms.TextInput(attrs={'class': 'form-control'}),
            'niveis_dificuldade': forms.Select(attrs={'class': 'form-select'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

        labels = {
            'modalidade': 'Modalidade*',
            'niveis_dificuldade': 'Níveis de Dificuldade*',
            'descricao': 'Descrição',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'


NIVEL_CHOICES_FILTER = [('', 'Todos')] + Servico.NIVEIS_DIFICULDADE_CHOICES

class ServicoFilterForm(forms.Form):
    modalidade = forms.CharField(
        required=False,
        label='Filtrar por Modalidade',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Parte do nome...'})
    )

    niveis_dificuldade = forms.ChoiceField(
        required=False,
        choices=NIVEL_CHOICES_FILTER,
        label='Filtrar por Nível',
        widget=forms.Select(attrs={'class': 'form-select'})
    )


class FuncionarioForm(forms.ModelForm):

    HORARIOS_CHOICES = [(f"{h:02d}:00", f"{h:02d}:00") for h in range(6, 21)]

    horarios_trabalho = forms.MultipleChoiceField(
        choices=HORARIOS_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label="Horários de Trabalho",
        required=False,
    )

    class Meta:
        model = Funcionario
        fields = [
            'nome',
            'cpf',
            'rg',
            'telefone',
            'email',
            'data_nascimento',
            'status',
            'funcao',
            'salario',
            'carga_horaria',
            'horarios_trabalho',
            'login',
            'senha',
            'is_admin',
        ]
    
    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        if not cpf.isdigit() or len(cpf) != 11:
            raise forms.ValidationError("CPF deve conter exatamente 11 dígitos numéricos.")
        return cpf

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Oculta campos senha e login da tela de edição
        if self.instance and self.instance.pk:
            self.fields.pop('login', None)
            self.fields.pop('senha', None)
            self.fields.pop('is_admin', None)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.enctype = 'multipart/form-data'
        self.helper.label_class = 'form-label'
        self.helper.layout = Layout(

            # Dados Pessoais
            Fieldset(
                "Dados Pessoais",
                Row(
                    Column('nome', css_class=COL_MD_6),
                    Column('cpf', css_class=COL_MD_6),
                    Column('data_nascimento', css_class=COL_MD_6),
                    Column('telefone', css_class=COL_MD_6),
                )
            ),

            # Dados Profissionais
            Fieldset(
                "Dados Profissionais",
                Row(
                    Column('funcao', css_class=COL_MD_6),
                    Column('carga_horaria', css_class=COL_MD_6),
                    Column('salario', css_class=COL_MD_6),
                    Column('data_contratacao', css_class=COL_MD_6),
                )
            ),

            # Acesso ao Sistema
            Fieldset(
                "Acesso ao Sistema",
                Row(
                    Column('login', css_class=COL_MD_6),
                    Column('senha', css_class=COL_MD_6),
                    Column('is_admin', css_class=COL_MD_6),
                )
            ),

            # Horários e Observações
            Fieldset(
                "Horários de Trabalho",
                'horarios_trabalho',
                'observacoes'
            ),

        )


class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = [
            'nome', 'cpf', 'rg', 'telefone', 'email', 'data_nascimento',
            'profissao', 'historico_saude', 'data_inicio_plano',
            'data_vencimento_plano', 'plano_ativo', 'plano'
        ]

    plano = forms.ModelChoiceField(
        queryset=Plano.objects.all(),
        empty_label="Selecione o Plano",
        required=True,
        label="Código do Plano",
        widget=forms.Select(attrs={'class': 'form-select'}),
        to_field_name='codigo'
    )


class PlanoForm(forms.ModelForm):
    class Meta:
        model = Plano
        fields = ['codigo', 'nome', 'qtd_aulas', 'valor_aula', 'status', 'limite_vigencia']


class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('login', 'Entrar', css_class='btn btn-primary w-100'))


class AulaForm(forms.ModelForm):
    class Meta:
        model = Aula
        fields = ['data', 'horario', 'servicos', 'funcionario']
        widgets = {
            'data': forms.DateInput(
                attrs={'type': 'date', 'min': date.today().isoformat()}
            ),
            'horario': forms.TimeInput(attrs={'type': 'time'}),
            'servicos': forms.CheckboxSelectMultiple(),
            'funcionario': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['funcionario'].required = True
        if self.instance and self.instance.pk:
            self.initial['data'] = self.instance.data.strftime('%Y-%m-%d')
            self.initial['horario'] = self.instance.horario.strftime('%H:%M')

    def clean(self):
        cleaned_data = super().clean()
        data = cleaned_data.get('data')
        horario = cleaned_data.get('horario')

        if data and horario:
            data_hora = datetime.combine(data, horario)
            if timezone.is_naive(data_hora):
                data_hora = timezone.make_aware(data_hora)

            agora = timezone.now()

            if data_hora < agora:
                raise forms.ValidationError('Não é possível agendar aulas para datas/horários passados.')


class AulaAlunoFrequenciaForm(forms.ModelForm):
    class Meta:
        model = AulaAluno
        fields = ['frequencia', 'evolucao_na_aula']
        widgets = {
            'frequencia': forms.CheckboxInput(),
            'evolucao_na_aula': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Descreva a evolução do aluno (se presente)...'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        frequencia = cleaned_data.get('frequencia')
        evolucao = cleaned_data.get('evolucao_na_aula')

        if not frequencia and evolucao:
            raise forms.ValidationError("Não é possível registrar evolução de aluno ausente.")

        if not frequencia:
            cleaned_data['evolucao_na_aula'] = ''  # Apaga a evolução indevidamente preenchida

        return cleaned_data


class ContaReceberForm(forms.ModelForm):
    class Meta:
        model = ContaReceber
        fields = ['aluno', 'valor', 'vencimento']

    aluno = forms.ModelChoiceField(
        queryset=Aluno.objects.all(),
        empty_label="Selecione o aluno",
        widget=forms.Select
    )
    vencimento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        input_formats=['%Y-%m-%d']
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.vencimento:
            self.initial['vencimento'] = self.instance.vencimento.strftime('%Y-%m-%d')
        if self.instance and self.instance.pk:
            self.fields['aluno'].disabled = True

class PagamentoForm(forms.ModelForm):
    class Meta:
        model = Pagamento
        fields = ['conta', 'data_pagamento', 'metodo_pagamento']
        widgets = {
            'data_pagamento': forms.DateInput(attrs={'type': 'date'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtra apenas contas pendentes
        self.fields['conta'].queryset = ContaReceber.objects.filter(status='pendente')

class HorarioDisponivelForm(forms.ModelForm):
    class Meta:
        model = HorarioDisponivel
        fields = ['data', 'horario_inicio', 'horario_fim', 'capacidade_maxima', 'servico', 'funcionario']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'horario_inicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'horario_fim': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control', 'required': False}),
            'capacidade_maxima': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}), # Limite maximo de 5
            'servico': forms.Select(attrs={'class': 'form-select'}),
            'funcionario': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'data': 'Data do Horário*',
            'horario_inicio': 'Horário de Início*',
            'horario_fim': 'Horário de Término (Opcional)',
            'capacidade_maxima': 'Capacidade Máxima*',
            'servico': 'Serviço/Modalidade',
            'funcionario': 'Professor Responsável',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Configuração para Crispy Forms
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('data', css_class=COL_MD_6_MB_3),
                Column('horario_inicio', css_class=COL_MD_6_MB_3),
            ),
            Row(
                Column('horario_fim', css_class=COL_MD_6_MB_3),
                Column('capacidade_maxima', css_class=COL_MD_6_MB_3),
            ),
            Row(
                Column('servico', css_class=COL_MD_6_MB_3),
                Column('funcionario', css_class=COL_MD_6_MB_3),
            ),
            Submit('submit', 'Salvar Horário', css_class='btn btn-primary')
        )
        # Define os querysets para os campos de chave estrangeira (FK)
        self.fields['servico'].queryset = Servico.objects.all().order_by('modalidade')
        self.fields['servico'].empty_label = "Selecione um Serviço"
        self.fields['funcionario'].queryset = Funcionario.objects.all().order_by('nome')
        self.fields['funcionario'].empty_label = "Selecione um Funcionário"

    def clean(self):
        cleaned_data = super().clean()
        data = cleaned_data.get('data')
        horario_inicio = cleaned_data.get('horario_inicio')
        horario_fim = cleaned_data.get('horario_fim')
        capacidade_maxima = cleaned_data.get('capacidade_maxima')

        # Validação para capacidade máxima (entre 1 e 5)
        if capacidade_maxima is not None and (capacidade_maxima < 1 or capacidade_maxima > 5):
            self.add_error('capacidade_maxima', 'A capacidade máxima deve ser entre 1 e 5 alunos.')

        # Validação para horários (se houver horário de fim, deve ser depois do início)
        if horario_inicio and horario_fim and horario_fim <= horario_inicio:
            self.add_error('horario_fim', 'O horário de término deve ser posterior ao horário de início.')

        # Validação para não cadastrar horários no passado
        if data and horario_inicio:
            data_hora_inicio = datetime.combine(data, horario_inicio)
            # Torna a data_hora_inicio ciente de fuso horário se for ingênua
            if timezone.is_naive(data_hora_inicio):
                data_hora_inicio = timezone.make_aware(data_hora_inicio)
            
            agora = timezone.now()
            if data_hora_inicio < agora:
                self.add_error(None, 'Não é possível cadastrar horários para datas/horários passados.')
        
        return cleaned_data
    

class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = ['horario_disponivel', 'aluno', 'cancelado', 'motivo_cancelamento']
        widgets = {
            'horario_disponivel': forms.Select(attrs={'class': 'form-select'}),
            'aluno': forms.Select(attrs={'class': 'form-select'}),
            'cancelado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'motivo_cancelamento': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'horario_disponivel': 'Horário da Aula*',
            'aluno': 'Aluno*',
            'cancelado': 'Agendamento Cancelado?',
            'motivo_cancelamento': 'Motivo do Cancelamento (se houver)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            FloatingField('horario_disponivel'),
            FloatingField('aluno'),
            Field('cancelado', css_class='form-check-input'),
            FloatingField('motivo_cancelamento'),
            Submit('submit', 'Salvar Agendamento', css_class='btn btn-primary mt-3')
        )
        self.fields['horario_disponivel'].queryset = HorarioDisponivel.objects.filter(data__gte=date.today()).order_by('data', 'horario_inicio')
        self.fields['horario_disponivel'].empty_label = "Selecione um Horário"
        self.fields['aluno'].queryset = Aluno.objects.all().order_by('nome')
        self.fields['aluno'].empty_label = "Selecione um Aluno"

    def clean(self):
        cleaned_data = super().clean()
        horario_disponivel = cleaned_data.get('horario_disponivel')
        aluno = cleaned_data.get('aluno')
        cancelado = cleaned_data.get('cancelado')

        if self.instance.pk is None and horario_disponivel and horario_disponivel.esta_cheio and not cancelado:
             self.add_error('horario_disponivel', 'Este horário não possui mais vagas disponíveis.')

        if self.instance.pk is None and horario_disponivel and aluno:
            if Agendamento.objects.filter(horario_disponivel=horario_disponivel, aluno=aluno, cancelado=False).exists():
                self.add_error(None, f'O aluno {aluno.nome} já está agendado para este horário.')
        elif self.instance.pk and horario_disponivel and aluno and self.instance.horario_disponivel != horario_disponivel:
            if horario_disponivel.esta_cheio and not cancelado:
                 self.add_error('horario_disponivel', 'O novo horário selecionado não possui mais vagas disponíveis.')

            if Agendamento.objects.filter(horario_disponivel=horario_disponivel, aluno=aluno, cancelado=False).exclude(pk=self.instance.pk).exists():
                 self.add_error(None, f'O aluno {aluno.nome} já está agendado para o novo horário selecionado.')

        return cleaned_data
