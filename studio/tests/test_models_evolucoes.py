from datetime import date, time, timedelta
from django.test import TestCase
from studio.models import AulaAluno, Aula, Aluno, Plano, Funcionario, Servico

TOMORROW = date.today() + timedelta(days=1)


class EvolucaoModelTestCase(TestCase):
    def setUp(self):
        plano = Plano.objects.create(
            codigo=1, nome="Mensal", qtd_aulas=10,
            valor_aula=100, limite_vigencia="M"
        )
        self.aluno = Aluno.objects.create(
            cpf="12312312300", nome="Carlos",
            data_nascimento=date(1990, 2, 2),
            profissao="Médico", historico_saude="Ok",
            data_inicio_plano=TOMORROW,
            data_vencimento_plano=TOMORROW + timedelta(days=30),
            plano=plano,
        )
        self.func = Funcionario.objects.create(
            cpf="99988877766", nome="Ana", data_nascimento=date(1990, 3, 3),
            funcao="Instrutora", salario=3000,
            carga_horaria=30, login="ana321", senha="senha123"
        )
        self.servico = Servico.objects.create(
            modalidade="Pilates", niveis_dificuldade="Iniciante"
        )
        self.aula = Aula.objects.create(
            data=TOMORROW, horario=time(15, 0), funcionario=self.func
        )
        self.aula.servicos.add(self.servico)

        self.aula_aluno = AulaAluno.objects.create(
            aula=self.aula, aluno=self.aluno,
            frequencia=True, evolucao_na_aula="Inicio alongamento"
        )

    def test_evolucao_salva(self):
        self.assertEqual(self.aula_aluno.evolucao_na_aula, "Inicio alongamento")