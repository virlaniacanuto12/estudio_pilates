from datetime import date, timedelta
from bs4 import BeautifulSoup
from django.test import TestCase
from django.urls import reverse
from studio.models import Aluno, Plano, ContaReceber
from django.contrib.messages import get_messages

class ContaReceberViewsTestCase(TestCase):
    def setUp(self):
        self.plano = Plano.objects.create(
            codigo=1,
            nome="Plano Mensal",
            qtd_aulas=10,
            valor_aula=50.0,
            status=True,
            limite_vigencia='M'
        )
        self.aluno1 = Aluno.objects.create(
            cpf="12345678900",
            nome="João",
            data_nascimento=date(1990, 1, 1),
            profissao="Professor",
            historico_saude="Nenhuma",
            data_inicio_plano=date.today(),
            data_vencimento_plano=date.today() + timedelta(days=30),
            plano=self.plano
        )
        self.aluno2 = Aluno.objects.create(
            cpf="98765432100",
            nome="Maria",
            data_nascimento=date(1995, 2, 2),
            profissao="Médica",
            historico_saude="Asma",
            data_inicio_plano=date.today(),
            data_vencimento_plano=date.today() + timedelta(days=30),
            plano=self.plano
        )
        self.conta_pendente = ContaReceber.objects.create(
            aluno=self.aluno1,
            valor=100,
            vencimento=date.today() + timedelta(days=10),
            status='pendente'
        )
        self.conta_pago = ContaReceber.objects.create(
            aluno=self.aluno2,
            valor=200,
            vencimento=date.today() - timedelta(days=10),
            status='pago'
        )

    def test_listar_contas_sem_filtros(self):
        url = reverse('studio:listar_contas')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.aluno1.nome)
        self.assertContains(response, self.aluno2.nome)

    def test_listar_contas_com_filtro_aluno(self):
        url = reverse('studio:listar_contas')
        response = self.client.get(url, {'aluno': self.aluno1.id})
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        table_text = soup.find('table').get_text()

        self.assertIn(self.aluno1.nome, table_text)
        self.assertNotIn(self.aluno2.nome, table_text)

    def test_listar_contas_com_filtro_estado(self):
        url = reverse('studio:listar_contas')
        response = self.client.get(url, {'estado': 'pendente'})
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        table_text = soup.find('table').get_text()

        self.assertIn(self.aluno1.nome, table_text)
        self.assertNotIn(self.aluno2.nome, table_text)

    def test_listar_contas_com_filtro_datas(self):
        url = reverse('studio:listar_contas')
        inicio = (date.today() - timedelta(days=5)).isoformat()
        fim = (date.today() + timedelta(days=15)).isoformat()
        response = self.client.get(url, {'inicio': inicio, 'fim': fim})
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')
        table_text = soup.find('table').get_text()

        self.assertIn(self.aluno1.nome, table_text)
        self.assertNotIn(self.aluno2.nome, table_text)

    def test_cadastrar_conta_post_valido(self):
        url = reverse('studio:registrar_conta')
        dados = {
            'aluno': self.aluno1.id,
            'valor': '150.00',
            'vencimento': date.today().isoformat(),
            'status': 'pendente'
        }
        response = self.client.post(url, dados)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ContaReceber.objects.count(), 3)

    def test_cadastrar_conta_post_invalido(self):
        url = reverse('studio:registrar_conta')
        dados = {
            'valor': '',
            'vencimento': '',
            'status': 'pago'
        }
        response = self.client.post(url, dados)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'studio/conta/registrar_conta.html')
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn('aluno', form.errors)
        self.assertIn('valor', form.errors)
        self.assertIn('vencimento', form.errors)

    def test_editar_conta_post_valido(self):
        url = reverse('studio:editar_conta', args=[self.conta_pendente.id])
        dados = {
            'aluno': self.aluno1.id,
            'valor': '250.00',
            'vencimento': (date.today() + timedelta(days=5)).isoformat(),
            'status': 'pendente'
        }
        response = self.client.post(url, dados)
        self.assertEqual(response.status_code, 302)
        self.conta_pendente.refresh_from_db()
        self.assertEqual(str(self.conta_pendente.valor), '250.00')

    def test_editar_conta_pago_redireciona(self):
        url = reverse('studio:editar_conta', args=[self.conta_pago.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("já foi paga" in str(m) for m in messages))

    def test_editar_conta_post_invalido(self):
        url = reverse('studio:editar_conta', args=[self.conta_pendente.id])
        dados = {
            'aluno': '',
            'valor': '',
            'vencimento': '',
            'status': 'pendente'
        }
        response = self.client.post(url, dados)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'studio/conta/registrar_conta.html')
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn('aluno', form.errors)
        self.assertIn('valor', form.errors)
        self.assertIn('vencimento', form.errors)
    def test_excluir_conta_post(self):
        url = reverse('studio:excluir_conta', args=[self.conta_pendente.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(ContaReceber.objects.filter(pk=self.conta_pendente.id).exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("excluída com sucesso" in str(m) for m in messages))
    def test_excluir_conta_get_not_allowed(self):
        url = reverse('studio:excluir_conta', args=[self.conta_pendente.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 405)
    def test_detalhar_conta(self):
        url = reverse('studio:detalhes_conta', args=[self.conta_pendente.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.aluno1.nome)
        self.assertTemplateUsed(response, 'studio/conta/detalhar_conta.html')
    def test_listar_contas_post_not_allowed(self):
        url = reverse('studio:listar_contas')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 405)


