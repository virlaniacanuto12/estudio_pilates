from datetime import date, timedelta
from django.test import TestCase
from studio.models import Aluno, Plano, ContaReceber, Pagamento

class PagamentoModelTestCase(TestCase):
    def setUp(self):
        self.plano = Plano.objects.create(
            codigo=1,
            nome="Mensal",
            qtd_aulas=12,
            valor_aula=50.0,
            status=True,
            limite_vigencia='M'
        )
        self.aluno = Aluno.objects.create(
            cpf="12345678901",
            nome="Carlos",
            data_nascimento=date(1992, 4, 15),
            profissao="Engenheiro",
            historico_saude="Nenhum",
            data_inicio_plano=date.today(),
            data_vencimento_plano=date.today() + timedelta(days=30),
            plano=self.plano
        )
        self.conta = ContaReceber.objects.create(
            aluno=self.aluno,
            valor=600.00,
            vencimento=date.today(),
            status='pendente'
        )

    def test_criar_pagamento_valido(self):
        pagamento = Pagamento.objects.create(
            conta=self.conta,
            data_pagamento=date.today(),
            metodo_pagamento='PIX',
            valor=600.00,
            status='Efetivado'
        )
        self.assertEqual(Pagamento.objects.count(), 1)
        self.assertEqual(str(pagamento), f'Pagamento #{pagamento.id} - {self.conta}')

    def test_pagamento_associado_a_conta(self):
        pagamento = Pagamento.objects.create(
            conta=self.conta,
            data_pagamento=date.today(),
            metodo_pagamento='Cartão',
            valor=600.00
        )
        self.assertEqual(pagamento.conta, self.conta)
        self.assertEqual(pagamento.conta.aluno.nome, "Carlos")

    def test_nao_permite_pagamento_duplicado_para_mesma_conta(self):
        Pagamento.objects.create(
            conta=self.conta,
            data_pagamento=date.today(),
            metodo_pagamento='PIX',
            valor=600.00
        )
        with self.assertRaises(Exception):
            Pagamento.objects.create(
                conta=self.conta,  # mesmo conta
                data_pagamento=date.today(),
                metodo_pagamento='Dinheiro',
                valor=600.00
            )

    def test_valores_e_metodos_validos(self):
        pagamento = Pagamento.objects.create(
            conta=self.conta,
            data_pagamento=date.today(),
            metodo_pagamento='Transferência',
            valor=600.00
        )
        self.assertEqual(pagamento.valor, 600.00)
        self.assertIn(pagamento.metodo_pagamento, dict(Pagamento.METODOS).keys())