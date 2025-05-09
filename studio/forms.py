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
    from django import forms
from .models import Funcionario

class FuncionarioForm(forms.ModelForm):
    senha = forms.CharField(widget=forms.PasswordInput(), required=False)

    class Meta:
        model = Funcionario
        fields = ['nome', 'cpf', 'rg', 'telefone', 'email', 'data_nascimento', 'funcao', 'salario', 
                  'carga_horaria', 'horarios_trabalho', 'login', 'senha', 'is_admin']

    def save(self, commit=True):
        funcionario = super().save(commit=False)
        if self.cleaned_data['senha']:
            funcionario.senha_hash = self.cleaned_data['senha']
        if commit:
            funcionario.save()
        return funcionario
