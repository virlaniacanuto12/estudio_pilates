from datetime import date, timedelta
from django.test import TestCase
from studio.models import Aluno, Plano


class AlunoModelTestCase(TestCase):
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

    def test_criacao_aluno(self):
        self.assertEqual(self.aluno.nome, "João Silva")
        self.assertEqual(self.aluno.plano.nome, "Plano Mensal")

    def test_str(self):
        self.assertEqual(str(self.aluno), "12345678900 (João Silva)")

    def test_calcular_idade(self):
        idade = self.aluno.calcular_idade()
        self.assertTrue(isinstance(idade, int))
        self.assertGreaterEqual(idade, 0)
