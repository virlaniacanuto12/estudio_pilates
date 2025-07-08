from datetime import date, timedelta
from django.test import TestCase
from studio.models import Aluno, Plano, ContaReceber


class ContaReceberModelTestCase(TestCase):
    def setUp(self):
        self.plano = Plano.objects.create(
            codigo=1,
            nome="Plano Mensal",
            qtd_aulas=12,
            valor_aula=50.0,
            status=True,
            limite_vigencia='M'
        )

        self.aluno = Aluno.objects.create(
            cpf="12345678900",
            nome="João Silva",
            data_nascimento=date(2000, 6, 1),
            profissao="Professor",
            historico_saude="Sem restrições",
            data_inicio_plano=date.today(),
            data_vencimento_plano=date.today() + timedelta(days=30),
            plano=self.plano
        )

    def test_criacao_conta_receber(self):
        conta = ContaReceber.objects.create(
            aluno=self.aluno,
            valor=150.00,
            vencimento=date.today() + timedelta(days=5),
            status='pendente'
        )
        self.assertEqual(conta.aluno.nome, "João Silva")
        self.assertEqual(conta.valor, 150.00)
        self.assertEqual(conta.status, 'pendente')

    def test_str_representation(self):
        conta = ContaReceber.objects.create(
            aluno=self.aluno,
            valor=100.00,
            vencimento=date(2025, 7, 31),
            status='pago'
        )
        expected = f"Conta de {self.aluno} - 2025-07-31 - PAGO"
        self.assertEqual(str(conta), expected)

    def test_estado_atual_pago(self):
        conta = ContaReceber.objects.create(
            aluno=self.aluno,
            valor=200.00,
            vencimento=date.today() - timedelta(days=10),
            status='pago'
        )
        self.assertEqual(conta.estado_atual, 'Pago')

    def test_estado_atual_vencido(self):
        conta = ContaReceber.objects.create(
            aluno=self.aluno,
            valor=200.00,
            vencimento=date.today() - timedelta(days=10),
            status='pendente'
        )
        self.assertEqual(conta.estado_atual, 'Vencido')

    def test_estado_atual_pendente(self):
        conta = ContaReceber.objects.create(
            aluno=self.aluno,
            valor=200.00,
            vencimento=date.today() + timedelta(days=5),
            status='pendente'
        )
        self.assertEqual(conta.estado_atual, 'Pendente')