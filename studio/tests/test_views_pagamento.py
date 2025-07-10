from datetime import date, timedelta
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from studio.models import Aluno, Plano, ContaReceber, Pagamento

class PagamentoViewsTestCase(TestCase):
    def setUp(self):
        self.plano = Plano.objects.create(
            codigo=1,
            nome="Mensal",
            qtd_aulas=10,
            valor_aula=50.0,
            status=True,
            limite_vigencia='M'
        )
        self.aluno = Aluno.objects.create(
            cpf="11122233344",
            nome="Ana",
            data_nascimento=date(1990, 5, 20),
            profissao="Designer",
            historico_saude="Nenhum",
            data_inicio_plano=date.today(),
            data_vencimento_plano=date.today() + timedelta(days=30),
            plano=self.plano
        )
        self.conta = ContaReceber.objects.create(
            aluno=self.aluno,
            valor=300.00,
            vencimento=date.today() + timedelta(days=5),
            status='pendente'
        )

    def test_get_registrar_pagamento_com_conta_id(self):
        url = reverse('studio:registrar_pagamento') + f'?conta_id={self.conta.id}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertContains(response, 'name="data_pagamento"')
        self.assertContains(response, 'name="conta"')

    def test_get_registrar_pagamento_sem_conta_id(self):
        url = reverse('studio:registrar_pagamento')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)

    def test_post_registrar_pagamento_valido(self):
        url = reverse('studio:registrar_pagamento')
        dados = {
            'conta': self.conta.id,
            'data_pagamento': timezone.now().date().strftime('%Y-%m-%d'),
            'metodo_pagamento': 'PIX',
            'valor': '999.99',  
        }
        response = self.client.post(url, dados)
        self.assertEqual(response.status_code, 302) 
        pagamento = Pagamento.objects.get(conta=self.conta)
        self.assertEqual(pagamento.valor, self.conta.valor)
        self.assertEqual(pagamento.status, 'Efetivado')
        self.conta.refresh_from_db()
        self.assertEqual(self.conta.status, 'pago')

    def test_post_registrar_pagamento_invalido(self):
        url = reverse('studio:registrar_pagamento')
        dados = {
            'conta': '', 
            'data_pagamento': '',
            'metodo_pagamento': '',
            'valor': '',
        }
        response = self.client.post(url, dados)
        self.assertEqual(response.status_code, 200) 
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn('conta', form.errors)
        self.assertIn('data_pagamento', form.errors)
        self.assertIn('metodo_pagamento', form.errors)

    def test_listar_pagamentos_sem_filtros(self):
        Pagamento.objects.create(
            conta=self.conta,
            data_pagamento=date.today(),
            metodo_pagamento='PIX',
            valor=self.conta.valor
        )
        url = reverse('studio:listar_pagamentos')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.aluno.nome)

    def test_listar_pagamentos_com_filtro_metodo(self):
        Pagamento.objects.create(
            conta=self.conta,
            data_pagamento=date.today(),
            metodo_pagamento='PIX',
            valor=self.conta.valor
        )
        url = reverse('studio:listar_pagamentos')
        response = self.client.get(url, {'metodo': 'PIX'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.aluno.nome)
        response = self.client.get(url, {'metodo': 'Dinheiro'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.aluno.nome)

    def test_listar_pagamentos_com_filtro_datas(self):
        pagamento = Pagamento.objects.create(
            conta=self.conta,
            data_pagamento=date.today(),
            metodo_pagamento='PIX',
            valor=self.conta.valor
        )
        url = reverse('studio:listar_pagamentos')
        inicio = (date.today() - timedelta(days=1)).isoformat()
        fim = (date.today() + timedelta(days=1)).isoformat()
        response = self.client.get(url, {'data_inicial': inicio, 'data_final': fim})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.aluno.nome)

    def test_listar_pagamentos_com_filtro_aluno(self):
        pagamento = Pagamento.objects.create(
            conta=self.conta,
            data_pagamento=date.today(),
            metodo_pagamento='PIX',
            valor=self.conta.valor
        )
        url = reverse('studio:listar_pagamentos')
        response = self.client.get(url, {'aluno': 'Ana'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.aluno.nome)
        response = self.client.get(url, {'aluno': 'NãoExiste'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.aluno.nome)
    def test_detalhes_pagamento(self):
        pagamento = Pagamento.objects.create(
            conta=self.conta,
            data_pagamento=date.today(),
            metodo_pagamento='PIX',
            valor=self.conta.valor
        )
        url = reverse('studio:detalhes_pagamento', args=[pagamento.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.aluno.nome)
        self.assertContains(response, 'PIX')
        self.assertContains(response, '300,00')
