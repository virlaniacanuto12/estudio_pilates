from django.shortcuts import render # Responsável por renderizar o template HTML
from .models import Servico       # Importa nosso modelo Servico

# Create your views here.

def listar_servicos(request):
    """
    Esta view busca todos os objetos Servico no banco de dados
    e os envia para o template 'studio/listar_servicos.html'.
    """
    # 1. Buscar os dados no banco usando o ORM do Django
    todos_servicos = Servico.objects.all().order_by('modalidade') # Pega todos e ordena por modalidade

    # 2. Preparar o contexto (um dicionário) para enviar os dados ao template
    contexto = {
        'lista_servicos': todos_servicos, # A chave 'lista_servicos' será usada no HTML
    }

    # 3. Renderizar o template HTML, passando a requisição e o contexto
    return render(request, 'studio/listar_servicos.html', contexto)