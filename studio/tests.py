# studio/tests.py

from django.test import TestCase, Client
from django.urls import reverse
from .models import Servico
from .forms import ServicoForm 
from django.contrib import messages
from .forms import ServicoForm, ServicoFilterForm 


class ServicoCreateViewTests(TestCase):

    def setUp(self):
        self.create_url = reverse('studio:novo_servico') 
        self.list_url = reverse('studio:lista_servicos')

    def test_create_view_get_request(self):
        """Testa se a página de criação de serviço carrega corretamente (GET)"""
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'studio/servicos/criar_servico.html')
        self.assertIsInstance(response.context['form'], ServicoForm)
        self.assertFalse(response.context['form'].is_bound)
        self.assertContains(response, '<form')
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_create_view_post_valid_data(self):
        """Testa a criação de um novo serviço com dados válidos (POST)"""
        servicos_count_before = Servico.objects.count()
        valid_data = {
            'modalidade': 'Pilates com Aparelhos Teste',
            'niveis_dificuldade': 'Intermediário', 
            'descricao': 'Aula de Pilates em aparelhos para nível intermediário.'
        }
        response = self.client.post(self.create_url, data=valid_data)
        self.assertEqual(response.status_code, 302) 
        self.assertRedirects(response, self.list_url) 
        self.assertEqual(Servico.objects.count(), servicos_count_before + 1)
        
        novo_servico = Servico.objects.latest('id')
        self.assertEqual(novo_servico.modalidade, 'Pilates com Aparelhos Teste')
        self.assertEqual(novo_servico.niveis_dificuldade, 'Intermediário')

    def test_create_view_post_invalid_data_missing_modalidade(self):
        """Testa a submissão de dados inválidos (modalidade faltando - POST)"""
        servicos_count_before = Servico.objects.count()
        invalid_data = {
            'modalidade': '', 
            'niveis_dificuldade': 'Iniciante',
            'descricao': 'Tentativa inválida.'
        }
        response = self.client.post(self.create_url, data=invalid_data)
        self.assertEqual(response.status_code, 200) 
        self.assertTemplateUsed(response, 'studio/servicos/criar_servico.html')
        self.assertTrue(response.context['form'].is_bound)
        self.assertFalse(response.context['form'].is_valid())
        self.assertTrue(response.context['form'].has_error('modalidade'))
        self.assertEqual(Servico.objects.count(), servicos_count_before) 

    def test_create_view_post_invalid_data_missing_nivel(self):
        """Testa a submissão de dados inválidos (nível faltando - POST)"""
        servicos_count_before = Servico.objects.count()
        invalid_data = {
            'modalidade': 'Funcional Teste',
            'niveis_dificuldade': '', 
            'descricao': 'Outra tentativa inválida.'
        }
        response = self.client.post(self.create_url, data=invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertTrue(response.context['form'].has_error('niveis_dificuldade'))
        self.assertEqual(Servico.objects.count(), servicos_count_before)
        

class ServicoListViewTests(TestCase): 

    @classmethod
    def setUpTestData(cls):
        cls.servico1 = Servico.objects.create(modalidade='Pilates Clássico', niveis_dificuldade='Iniciante', descricao='Para iniciantes em Pilates')
        cls.servico2 = Servico.objects.create(modalidade='Reformer Avançado', niveis_dificuldade='Avançado', descricao='Desafios no Reformer')
        cls.servico3 = Servico.objects.create(modalidade='Pilates Solo', niveis_dificuldade='Intermediário', descricao='Fortalecimento e flexibilidade')

    def setUp(self):
        self.list_url = reverse('studio:lista_servicos')

    def test_list_view_status_code_and_name(self):
        """Testa se a URL principal e a nomeada dos serviços respondem com 200 OK"""
        response_named = self.client.get(self.list_url)
        self.assertEqual(response_named.status_code, 200)

    def test_list_view_uses_correct_template(self):
        """Testa se a view renderiza o template correto"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'studio/servicos/lista_servicos.html')

    def test_list_displays_all_services_initially(self):
        """Testa se todos os serviços criados aparecem na página inicialmente"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Pilates Clássico')
        self.assertContains(response, 'Reformer Avançado')
        self.assertContains(response, 'Pilates Solo')

    def test_list_context_data_initial(self):
        """Testa os dados de contexto iniciais (sem filtros)"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('lista_servicos' in response.context)
        self.assertEqual(len(response.context['lista_servicos']), 3) #
        self.assertTrue('filter_form' in response.context)
        self.assertIsInstance(response.context['filter_form'], ServicoFilterForm)

    def test_list_filter_by_modalidade_exact(self):
        """Testa o filtro por uma modalidade exata que existe"""
        response = self.client.get(self.list_url + '?modalidade=Pilates+Clássico')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Pilates Clássico')
        self.assertNotContains(response, 'Reformer Avançado')
        self.assertEqual(len(response.context['lista_servicos']), 1)
        self.assertEqual(response.context['filter_form']['modalidade'].value(), 'Pilates Clássico')

    def test_list_filter_by_modalidade_partial_icontains(self):
        """Testa o filtro por parte da modalidade (case-insensitive)"""
        response = self.client.get(self.list_url + '?modalidade=pilates') # "pilates" em minúsculo
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Pilates Clássico')
        self.assertContains(response, 'Pilates Solo')
        self.assertNotContains(response, 'Reformer Avançado') # Não contém "pilates"
        self.assertEqual(len(response.context['lista_servicos']), 2)

    def test_list_filter_by_niveis_dificuldade_exact(self):
        """Testa o filtro por um nível de dificuldade exato"""
        response = self.client.get(self.list_url + '?niveis_dificuldade=Avançado')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Reformer Avançado')
        self.assertNotContains(response, 'Pilates Clássico')
        self.assertEqual(len(response.context['lista_servicos']), 1)
        self.assertEqual(response.context['filter_form']['niveis_dificuldade'].value(), 'Avançado')

    def test_list_filter_by_modalidade_and_niveis(self):
        """Testa o filtro combinado de modalidade e nível"""
        response = self.client.get(self.list_url + '?modalidade=Pilates&niveis_dificuldade=Iniciante')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Pilates Clássico')
        self.assertNotContains(response, 'Reformer Avançado')
        self.assertNotContains(response, 'Pilates Solo')
        self.assertEqual(len(response.context['lista_servicos']), 1)

    def test_list_filter_no_results(self):
        """Testa um filtro que não deve retornar nenhum serviço"""
        response = self.client.get(self.list_url + '?modalidade=YogaInexistente')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['lista_servicos']), 0)
        self.assertContains(response, 'Nenhum serviço encontrado com os filtros aplicados.')

    def test_list_empty_when_no_services_exist(self):
        """Testa a listagem quando não há nenhum serviço no banco."""
        Servico.objects.all().delete() # Apaga todos os serviços
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['lista_servicos']), 0)
        self.assertContains(response, 'Nenhum serviço cadastrado ainda.')


class ServicoUpdateViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.servico_existente = Servico.objects.create(
            modalidade='Pilates de Edição',
            niveis_dificuldade='Intermediário',
            descricao='Serviço para testar edição'
        )

    def setUp(self):
        self.list_url = reverse('studio:lista_servicos')
        self.edit_url_valid_pk = reverse('studio:editar_servico', args=[self.servico_existente.pk])
        self.edit_url_invalid_pk = reverse('studio:editar_servico', args=[999]) 

    def test_edit_view_get_existing_pk(self):
        """Testa o GET na view de edição para um serviço existente."""
        response = self.client.get(self.edit_url_valid_pk)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'studio/servicos/criar_servico.html') 
        self.assertIsInstance(response.context['form'], ServicoForm)
        self.assertEqual(response.context['form'].instance, self.servico_existente) 

    def test_edit_view_get_non_existent_pk(self):
        """Testa o GET na view de edição para um serviço que NÃO existe (deve ser 404)."""
        response = self.client.get(self.edit_url_invalid_pk)
        self.assertEqual(response.status_code, 404)

    def test_edit_view_post_valid_data(self):
        """Testa o POST na view de edição com dados válidos."""
        dados_atualizados = {
            'modalidade': 'Pilates Editado com Sucesso',
            'niveis_dificuldade': 'Avançado',
            'descricao': 'Descrição atualizada.'
        }
        response = self.client.post(self.edit_url_valid_pk, data=dados_atualizados)
        self.assertEqual(response.status_code, 302) 
        self.assertRedirects(response, self.list_url)
        self.servico_existente.refresh_from_db() 
        self.assertEqual(self.servico_existente.modalidade, 'Pilates Editado com Sucesso')
        self.assertEqual(self.servico_existente.niveis_dificuldade, 'Avançado')

    def test_edit_view_post_invalid_data_missing_modalidade(self):
        """Testa o POST na view de edição com modalidade faltando."""
        modalidade_original = self.servico_existente.modalidade     
        dados_invalidos = {
            'modalidade': '', # Inválido
            'niveis_dificuldade': 'Avançado',
            'descricao': 'Tentativa de edição inválida.'
        }
        response = self.client.post(self.edit_url_valid_pk, data=dados_invalidos)
        self.assertEqual(response.status_code, 200) 
        self.assertTemplateUsed(response, 'studio/servicos/criar_servico.html')
        self.assertFalse(response.context['form'].is_valid())
        self.assertTrue(response.context['form'].has_error('modalidade'))
        self.servico_existente.refresh_from_db()
        self.assertEqual(self.servico_existente.modalidade, modalidade_original)


class ServicoDeleteViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.servico_para_excluir = Servico.objects.create(
            modalidade='Pilates para Excluir',
            niveis_dificuldade='Iniciante',
            descricao='Este serviço será excluído nos testes.'
        )
        cls.outro_servico = Servico.objects.create(
            modalidade='Outro Pilates',
            niveis_dificuldade='Intermediário'
        )

    def setUp(self):
        self.list_url = reverse('studio:lista_servicos')
        self.delete_url_valid_pk = reverse('studio:excluir_servico', args=[self.servico_para_excluir.pk])
        self.delete_url_invalid_pk = reverse('studio:excluir_servico', args=[999]) # PK que não existe

    def test_delete_view_get_request_redirects(self):
        """Testa se um GET para a URL de exclusão redireciona e não exclui."""
        servicos_count_before = Servico.objects.count()
        response = self.client.get(self.delete_url_valid_pk)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.list_url)
        self.assertEqual(Servico.objects.count(), servicos_count_before)

    def test_delete_view_post_deletes_service_and_redirects(self):
        """Testa se um POST para a URL de exclusão exclui o serviço e redireciona."""
        servicos_count_before = Servico.objects.count()
        response = self.client.post(self.delete_url_valid_pk)
        self.assertEqual(response.status_code, 302) 
        self.assertRedirects(response, self.list_url)
        self.assertEqual(Servico.objects.count(), servicos_count_before - 1)
        with self.assertRaises(Servico.DoesNotExist):
            Servico.objects.get(pk=self.servico_para_excluir.pk)

    def test_delete_view_post_non_existent_pk(self):
        """Testa o POST para a URL de exclusão com um PK que NÃO existe (deve ser 404)."""
        response = self.client.post(self.delete_url_invalid_pk)
        self.assertEqual(response.status_code, 404)