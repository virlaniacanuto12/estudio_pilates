from datetime import date, time, timedelta
from django.test import TestCase
from django.urls import reverse
from studio.models import Aluno, Aula, AulaAluno, Funcionario, Servico

TOMORROW = date.today() + timedelta(days=1)


class EvolucoesAlunoViewTestCase(TestCase):
    def setUp(self):
        self.func = Funcionario.objects.create(
            cpf="12345678900", nome="Instrutor", data_nascimento=date(1980, 1, 1),
            funcao="Instrutor", salario=2000, carga_horaria=40,
            login="instrutor1", senha="senha123"
        )
        self.servico = Servico.objects.create(
            modalidade="Pilates", niveis_dificuldade="Iniciante"
        )
        self.aluno = Aluno.objects.create(
            cpf="11111111111", nome="Aluno Evolucao",
            data_nascimento=date(1995, 5, 5), profissao="Estudante",
            historico_saude="Ok",
            data_inicio_plano=TOMORROW, data_vencimento_plano=TOMORROW + timedelta(days=30),
            plano_ativo=True,
        )
        self.aula1 = Aula.objects.create(
            data=TOMORROW, horario=time(9, 0), funcionario=self.func
        )
        self.aula1.servicos.add(self.servico)
        self.aula2 = Aula.objects.create(
            data=TOMORROW, horario=time(10, 0), funcionario=self.func
        )
        self.aula2.servicos.add(self.servico)

        AulaAluno.objects.create(
            aula=self.aula1, aluno=self.aluno, frequencia=True,
            evolucao_na_aula="Melhorou postura"
        )
        AulaAluno.objects.create(
            aula=self.aula2, aluno=self.aluno, frequencia=True,
            evolucao_na_aula=""       
        )

    def test_evolucoes_view(self):
        resp = self.client.get(reverse("studio:evolucoes_aluno", args=[self.aluno.id]))
        self.assertEqual(resp.status_code, 200)
        evolucoes = resp.context["evolucoes"]
        self.assertEqual(len(evolucoes), 1)
        self.assertEqual(evolucoes[0][1], "Melhorou postura")
        self.assertEqual(evolucoes[0][0], self.aula1)