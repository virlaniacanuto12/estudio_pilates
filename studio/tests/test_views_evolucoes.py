from datetime import date, time
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from studio.models import Aluno, Aula, AulaAluno, Funcionario

class EvolucoesAlunoViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

        self.funcionario = Funcionario.objects.create(
            cpf="12345678900",
            nome="Instrutor Teste",
            data_nascimento=date(1980, 1, 1),
            funcao="Instrutor",
            salario=2000.0,
            carga_horaria=40,
            login="instrutor1",
            senha="senha123"
        )
        self.aluno = Aluno.objects.create(
            cpf="11111111111",
            nome="Aluno Evolucao",
            data_nascimento=date(1995, 5, 5),
            profissao="Estudante",
            historico_saude="Sem restrições",
            data_inicio_plano=date.today(),
            data_vencimento_plano=date.today(),
            plano_ativo=True
        )
        self.aula1 = Aula.objects.create(
            data=date.today(),
            horario=time(9, 0),
            funcionario=self.funcionario
        )
        self.aula2 = Aula.objects.create(
            data=date.today(),
            horario=time(10, 0),
            funcionario=self.funcionario
        )
        AulaAluno.objects.create(
            aula=self.aula1,
            aluno=self.aluno,
            frequencia=True,
            evolucao_na_aula="Melhorou muito a postura"
        )
        AulaAluno.objects.create(
            aula=self.aula2,
            aluno=self.aluno,
            frequencia=True,
            evolucao_na_aula=""
        )
        AulaAluno.objects.create(
            aula=self.aula2,
            aluno=self.aluno,
            frequencia=True,
            evolucao_na_aula=""
        )

    def test_evolucoes_aluno_view(self):
        url = reverse('studio:evolucoes_aluno', args=[self.aluno.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['aluno'], self.aluno)

        evolucoes = response.context['evolucoes']
        self.assertEqual(len(evolucoes), 1)
        self.assertEqual(evolucoes[0][1], "Melhorou muito a postura")
        self.assertEqual(evolucoes[0][0], self.aula1)