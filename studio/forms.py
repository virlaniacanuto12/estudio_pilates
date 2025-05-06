# studio/forms.py
from django import forms
from .models import Servico
from .models import Funcionario

class ServicoForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = ['modalidade', 'niveis_dificuldade', 'descricao'] # Atualizado o nome do campo

        widgets = {
            'modalidade': forms.TextInput(attrs={'class': 'form-control'}),
            'niveis_dificuldade': forms.Select(attrs={'class': 'form-select'}), # Mudado para Select por causa do 'choices' no model
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

        labels = {
            'modalidade': 'Modalidade*',
            'niveis_dificuldade': 'Níveis de Dificuldade*', # Atualizado nome e label (adicionado *)
            'descricao': 'Descrição',
        }

# Prepara as opções para o filtro de nível, adicionando uma opção "Todos"
NIVEL_CHOICES_FILTER = [('', 'Todos')] + Servico.NIVEIS_DIFICULDADE_CHOICES

class ServicoFilterForm(forms.Form):
    # Campo para buscar texto dentro da modalidade
    modalidade = forms.CharField(
        required=False, # Não obrigatório
        label='Filtrar por Modalidade',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Parte do nome...'})
    )
    # Campo para selecionar um nível de dificuldade específico
    niveis_dificuldade = forms.ChoiceField(
        required=False, # Não obrigatório
        choices=NIVEL_CHOICES_FILTER, # Usa a lista com a opção "Todos"
        label='Filtrar por Nível',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = '__all__'
