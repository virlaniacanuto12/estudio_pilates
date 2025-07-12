import datetime
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from studio.models import Funcionario 

from datetime import date 

class FuncionarioViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        # Cria um funcionário para usar nos testes de edição/exclusão/listagem
        self.funcionario_existente = Funcionario.objects.create(
            cpf="11111111111",              # Apenas números para passar na validação do clean_cpf
            rg="111111111",                
            nome="Funcionario Teste",
            telefone="11987654321",
            email="teste@funcionario.com",
            data_nascimento=date(1990, 5, 15),
            status=True,                   
            funcao="Professor",
            salario=2500.00,                
            carga_horaria=40.0,             
            horarios_trabalho="08:00,09:00,10:00", 
            login="teste_func",
            senha="senha_segura123",
            is_admin=False,
            
        )

        self.dados_funcionario_valido = {
            'nome': "Novo Funcionario",
            'cpf': "22222222222", 
            'rg': "222222222",
            'telefone': "22987654321",
            'email': "novo@funcionario.com",
            'data_nascimento': "1985-01-01", 
            'status': True,
            'funcao': "Recepcionista",
            'salario': 1800.00,
            'carga_horaria': 30.0,
            'horarios_trabalho': ['09:00', '10:00'], 
            'login': "novo_func",
            'senha': "outrasenhaforte",
            'is_admin': False,
        }

        self.dados_funcionario_invalido_cpf = {
            'nome': "Maria Teste",
            'cpf': "123", 
            'rg': "333333333",
            'telefone': "33987654321",
            'email': "maria@teste.com",
            'data_nascimento': "1990-01-01",
            'status': True,
            'funcao': "Programador",
            'salario': 3000.00,
            'carga_horaria': 40.0,
            'horarios_trabalho': ['11:00', '12:00'],
            'login': "mteste",
            'senha': "senhaforte",
            'is_admin': False,
        }

        self.dados_edicao_invalida = {
            'nome': "", 
            'email': "email_invalido", 
            'salario': "xyz", 
            'cpf': self.funcionario_existente.cpf, 
            'rg': self.funcionario_existente.rg,
            'telefone': self.funcionario_existente.telefone,
            'data_nascimento': self.funcionario_existente.data_nascimento.strftime('%Y-%m-%d'),
            'status': self.funcionario_existente.status,
            'funcao': self.funcionario_existente.funcao,
            'carga_horaria': self.funcionario_existente.carga_horaria,
            'horarios_trabalho': ["13:00"], 
            
        }


    # --- Testes para a View de listar_funcionario ---
    def test_listar_funcionario_GET(self):
        url = reverse('studio:listar_funcionario')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'studio/funcionario/listar_funcionario.html')
        self.assertIn('funcionario', response.context)
        self.assertContains(response, self.funcionario_existente.nome)

    # --- Testes para a View de Cadastro ---
    def test_cadastro_funcionario_GET(self):
        url = reverse('studio:cadastro_funcionario')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'studio/funcionario/cadastro_funcionario.html')
        self.assertIn('form', response.context) # Verifica se o formulário está no contexto

    def test_cadastro_funcionario_POST_valido(self):
        url = reverse('studio:cadastro_funcionario')
        funcionarios_antes = Funcionario.objects.count()
        response = self.client.post(url, data=self.dados_funcionario_valido)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Funcionario.objects.count(), funcionarios_antes + 1)
        self.assertRedirects(response, reverse('studio:listar_funcionario'))
        
        novo_funcionario = Funcionario.objects.get(cpf=self.dados_funcionario_valido['cpf'])
        self.assertEqual(novo_funcionario.nome, self.dados_funcionario_valido['nome'])
        self.assertEqual(novo_funcionario.email, self.dados_funcionario_valido['email'])
        


    def test_cadastro_funcionario_POST_invalido(self):
        url = reverse('studio:cadastro_funcionario')
        funcionarios_antes = Funcionario.objects.count()
        response = self.client.post(url, data=self.dados_funcionario_invalido_cpf)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'studio/funcionario/cadastro_funcionario.html')
        self.assertEqual(Funcionario.objects.count(), funcionarios_antes)
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn('cpf', form.errors) 


    # --- Testes para a View de Edição (editar_funcionario) ---
    def test_editar_funcionario_GET(self):
        url = reverse('studio:editar_funcionario', args=[self.funcionario_existente.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'studio/funcionario/editar_funcionario.html')
        self.assertIn('form', response.context)
        self.assertEqual(response.context['funcionario'], self.funcionario_existente)

    def test_editar_funcionario_POST_valido(self):
        url = reverse('studio:editar_funcionario', args=[self.funcionario_existente.id])
        
        dados_para_edicao = {
            'nome': "Nome Atualizado",
            'email': "atualizado@funcionario.com",
            'cpf': self.funcionario_existente.cpf, 
            'rg': self.funcionario_existente.rg,
            'telefone': self.funcionario_existente.telefone,
            'data_nascimento': self.funcionario_existente.data_nascimento.strftime('%Y-%m-%d'),
            'status': self.funcionario_existente.status,
            'funcao': self.funcionario_existente.funcao,
            'salario': self.funcionario_existente.salario,
            'carga_horaria': self.funcionario_existente.carga_horaria,
            'horarios_trabalho': ["14:00", "15:00"],
        }

        response = self.client.post(url, data=dados_para_edicao)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('studio:listar_funcionario'))

        self.funcionario_existente.refresh_from_db()
        self.assertEqual(self.funcionario_existente.nome, "Nome Atualizado")
        self.assertEqual(self.funcionario_existente.email, "atualizado@funcionario.com")


    def test_editar_funcionario_POST_invalido(self):
        url = reverse('studio:editar_funcionario', args=[self.funcionario_existente.id])
        response = self.client.post(url, data=self.dados_edicao_invalida)

        self.assertEqual(response.status_code, 200) 
        self.assertTemplateUsed(response, 'studio/funcionario/editar_funcionario.html')
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn('nome', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('salario', form.errors) 


    def test_editar_funcionario_GET_not_found(self):
        url = reverse('studio:editar_funcionario', args=[9999]) 
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404) 

    # --- Testes para a View de excluir_funcionario ---
    def test_excluir_funcionario_POST(self):
        temp_funcionario = Funcionario.objects.create(
            cpf="33333333333",
            rg="333333333",
            nome="Funcionario Para Excluir",
            telefone="33987654321",
            email="excluir@funcionario.com",
            data_nascimento=date(1995, 1, 1),
            status=True,
            funcao="Estagiario",
            salario=1000.00,
            carga_horaria=20.0,
            horarios_trabalho="13:00,14:00",
            login="func_excluir",
            senha="senha_do_excluir",
            is_admin=False,
        )
        funcionarios_antes = Funcionario.objects.count()
        url = reverse('studio:excluir_funcionario', args=[temp_funcionario.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('studio:listar_funcionario'))
        self.assertEqual(Funcionario.objects.count(), funcionarios_antes - 1)
        with self.assertRaises(Funcionario.DoesNotExist):
            Funcionario.objects.get(id=temp_funcionario.id)
        
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Funcionário excluído com sucesso!")

    def test_excluir_funcionario_GET_not_allowed(self):
        url = reverse('studio:excluir_funcionario', args=[self.funcionario_existente.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 405)

    def test_excluir_funcionario_POST_not_found(self):
        url = reverse('studio:excluir_funcionario', args=[9999])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)