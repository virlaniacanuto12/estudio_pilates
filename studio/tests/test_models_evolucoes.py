from django.test import TestCase
from studio.models import AulaAluno, Aula, Aluno, Plano, Funcionario, Servico
from datetime import date, time, timedelta

class EvolucaoModelTestCase(TestCase):
    def setUp(self):
        plano = Plano.objects.create(
            codigo=1,
            nome="Mensal",
            qtd_aulas=10,
            valor_aula=100,
            limite_vigencia='M'
        )

        self.aluno = Aluno.objects.create(
            cpf="12312312300",
            rg="1212121",
            nome="Carlos",
            telefone="83990000000",
            email="carlos@email.com",
            data_nascimento=date(1990, 2, 2),
            profissao="Médico",
            historico_saude="Leve dor na coluna",
            data_inicio_plano=date.today(),
            data_vencimento_plano=date.today() + timedelta(days=30),
            plano=plano
        )

        self.funcionario = Funcionario.objects.create(
            cpf="99988877766",
            rg="987654",
            nome="Ana",
            telefone="83999998888",
            email="ana@email.com",
            data_nascimento=date(1990, 3, 3),
            funcao="Instrutora",
            salario=3000.00,
            carga_horaria=30,
            login="ana321",
            senha="senha123"
        )

        self.aula = Aula.objects.create(
            data=date.today(),
            horario=time(15, 0),
            funcionario=self.funcionario
        )

        self.aula_aluno = AulaAluno.objects.create(
            aula=self.aula,
            aluno=self.aluno,
            frequencia=False,
            evolucao_na_aula="Início do alongamento"
        )

    def test_evolucao_na_aula(self):
        self.assertEqual(self.aula_aluno.evolucao_na_aula, "Início do alongamento")