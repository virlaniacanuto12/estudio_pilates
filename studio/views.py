# studio/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Servico
from .forms import ServicoForm, ServicoFilterForm
from .models import Funcionario
from .forms import FuncionarioForm 

# --- View listar_servicos ATUALIZADA ---
def lista_servicos(request):
    """
    Lista os serviços, aplicando filtros de modalidade e nível
    enviados via GET através do ServicoFilterForm.
    """
    # 1. Começa com todos os serviços
    queryset = Servico.objects.all()

    # 2. Instancia o formulário de filtro com os dados GET (se houver)
    # request.GET contém os parâmetros da URL (ex: ?modalidade=Pilates&niveis_dificuldade=Iniciante)
    filter_form = ServicoFilterForm(request.GET or None)

    # 3. Verifica se o formulário de filtro foi preenchido (é opcional validar aqui,
    #    mas útil se tivéssemos validações mais complexas)
    #    e aplica os filtros ao queryset se os campos tiverem valores.
    if filter_form.is_valid():
        modalidade = filter_form.cleaned_data.get('modalidade')
        niveis = filter_form.cleaned_data.get('niveis_dificuldade')

        # Aplica filtro de modalidade (busca case-insensitive que contenha o texto)
        if modalidade:
            queryset = queryset.filter(modalidade__icontains=modalidade)

        # Aplica filtro de nível de dificuldade (busca exata)
        if niveis: # Verifica se um nível foi selecionado (não é a string vazia de "Todos")
            queryset = queryset.filter(niveis_dificuldade=niveis)

    # 4. Ordena o resultado final
    queryset = queryset.order_by('modalidade')

    # 5. Prepara o contexto para enviar ao template
    #    Envia tanto a lista filtrada quanto o formulário de filtro
    contexto = {
        'lista_servicos': queryset,   # Agora contém a lista potencialmente filtrada
        'filter_form': filter_form, # Passa o formulário para ser exibido no template
    }

    # 6. Renderiza o template
    return render(request, 'studio/servicos/lista_servicos.html', contexto)
# --- Fim da View listar_servicos ATUALIZADA ---


# ... (views criar_servico, editar_servico, excluir_servico existentes) ...

# --- Nova View ---
def novo_servico(request):
    """
    Esta view lida com a exibição do formulário para criar um novo serviço (GET)
    e com o processamento dos dados enviados pelo formulário (POST).
    """
    if request.method == 'POST':
        # Se o formulário foi enviado (método POST)
        form = ServicoForm(request.POST) # Cria uma instância do form com os dados enviados
        if form.is_valid(): # Verifica se os dados são válidos
            form.save() # Salva o novo objeto Servico no banco de dados
            # Redireciona para a página de listagem de serviços após salvar
            return redirect('studio:lista_servicos')
        # Se o form não for válido, ele será renderizado novamente na página,
        # mostrando os erros (o código abaixo cuidará disso)
    else:
        # Se for a primeira vez acessando a página (método GET)
        form = ServicoForm() # Cria uma instância vazia do formulário

    # Prepara o contexto para enviar o formulário ao template
    contexto = {
        'form': form,
    }
    # Renderiza o template 'criar_servico.html', passando o form
    return render(request, 'studio/servicos/criar_servico.html', contexto)

# --- Nova View para Editar ---
def editar_servico(request, pk):
    """
    Busca um serviço existente pelo seu 'pk' (primary key),
    exibe o formulário preenchido (GET) e salva as alterações (POST).
    """
    # Busca o objeto Servico com o 'pk' fornecido, ou retorna erro 404 se não encontrar
    servico = get_object_or_404(Servico, pk=pk)

    if request.method == 'POST':
        # Cria o form com os dados enviados E associado ao objeto existente (instance=servico)
        form = ServicoForm(request.POST, instance=servico)
        if form.is_valid():
            form.save() # Salva as alterações no objeto 'servico' existente
            return redirect('studio:lista_servicos') # Redireciona para a lista
        # Se inválido, renderiza o template com o form contendo os erros (abaixo)
    else:
        # Método GET: Cria o form preenchido com os dados do objeto 'servico' existente
        form = ServicoForm(instance=servico)

    # Prepara o contexto (igual à view de criar, mas o 'form' estará preenchido no GET)
    contexto = {
        'form': form,
        # Poderíamos adicionar o 'servico' ao contexto se quiséssemos usar
        # outras informações dele no template, como o título da página.
        # 'servico': servico
    }
    # Reutiliza o mesmo template do formulário de criação
    return render(request, 'studio/servicos/criar_servico.html', contexto)

def excluir_servico(request, pk):
    servico = get_object_or_404(Servico, pk=pk)

    if request.method == 'POST':
        modalidade_servico = servico.modalidade
        servico.delete()
        # Adiciona a mensagem de sucesso aqui:
        messages.success(request, f'Serviço "{modalidade_servico}" excluído com sucesso.') # <--- USO DA FUNÇÃO
        return redirect('studio:lista_servicos')
    else:
        return redirect('studio:lista_servicos')


# View Funcionario 
def criar_funcionario(request):
    form = FuncionarioForm()
    if request.method == 'POST':
        form = FuncionarioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # redirecionar ou exibir mensagem
    return render(request, 'studio/funcionario/criar_funcionario.html', {'form': form})

def home(request):
    return render(request, 'studio/home.html')