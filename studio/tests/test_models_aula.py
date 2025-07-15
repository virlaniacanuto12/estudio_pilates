from datetime import date, time, timedelta
from django.test import TestCase
from studio.models import (
    Aula, AulaAluno, Aluno, Funcionario, Servico,
    HorarioDisponivel, Agendamento
)

TOMORROW = date.today() + timedelta(days=1)


class AulaModelTestCase(TestCase):
    def setUp(self):
        self.funcionario = Funcionario.objects.create(
            cpf="12345678900",
            nome="Funcionário Teste",
            data_nascimento=date(1990, 1, 1),
            funcao="Instrutor",
            salario=3000,
            carga_horaria=40,
            login="func1",
            senha="senha123",
        )

        self.servico = Servico.objects.create(
            modalidade="Pilates",
            niveis_dificuldade="Iniciante",
            descricao="Pilates solo",
        )

        self.aula = Aula.objects.create(
            data=TOMORROW,
            horario=time(10, 0),
            funcionario=self.funcionario,
        )
        self.aula.servicos.add(self.servico)

        self.aluno1 = Aluno.objects.create(
            cpf="11111111111",
            nome="Aluno Um",
            data_nascimento=date(2000, 1, 1),
            profissao="Estudante",
            historico_saude="Ok",
            data_inicio_plano=TOMORROW,
            data_vencimento_plano=TOMORROW + timedelta(days=30),
            plano_ativo=True,
        )
        self.aluno2 = Aluno.objects.create(
            cpf="22222222222",
            nome="Aluno Dois",
            data_nascimento=date(1995, 5, 5),
            profissao="Professor",
            historico_saude="Ok",
            data_inicio_plano=TOMORROW,
            data_vencimento_plano=TOMORROW + timedelta(days=30),
            plano_ativo=True,
        )

        self.horario = HorarioDisponivel.objects.create(
            data=TOMORROW,
            horario_inicio=time(10, 0),
            capacidade_maxima=10,
            servico=self.servico,
            funcionario=self.funcionario,
        )

        Agendamento.objects.create(horario_disponivel=self.horario, aluno=self.aluno1)
        Agendamento.objects.create(horario_disponivel=self.horario, aluno=self.aluno2)

    def test_aula_str(self):
        self.assertIn("Aula", str(self.aula))
        self.assertIn(str(self.aula.codigo), str(self.aula))

    def test_aula_cancelar(self):
        self.aula.cancelar()
        self.assertTrue(self.aula.cancelada)

    def test_participacoes_via_signal(self):
        participacoes = AulaAluno.objects.filter(aula=self.aula)
        self.assertEqual(participacoes.count(), 2)

    def test_total_presentes_e_ausentes(self):
        p1 = AulaAluno.objects.get(aula=self.aula, aluno=self.aluno1)
        p2 = AulaAluno.objects.get(aula=self.aula, aluno=self.aluno2)
        p1.marcar_presenca()
        self.assertEqual(self.aula.total_presentes(), 1)
        self.assertEqual(self.aula.total_ausentes(), 1)

    def test_lista_alunos(self):
        lista = self.aula.lista_alunos()
        self.assertIn(self.aluno1, lista)
        self.assertIn(self.aluno2, lista)

    def test_aulaaluno_str_e_status(self):
        p = AulaAluno.objects.get(aula=self.aula, aluno=self.aluno1)
        self.assertIn(self.aluno1.nome, str(p))
        self.assertIn("Ausente", p.status_presenca())
        p.marcar_presenca()
        self.assertIn("Presente", p.status_presenca())