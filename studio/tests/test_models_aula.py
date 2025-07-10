from django.test import TestCase
from django.utils import timezone
from datetime import date, time
from studio.models import Aula, AulaAluno, Aluno, Funcionario, Servico, HorarioDisponivel, Agendamento

class AulaModelTestCase(TestCase):

    def setUp(self):
        # Cria funcionário
        self.funcionario = Funcionario.objects.create(
            cpf="12345678900",
            nome="Funcionario Teste",
            data_nascimento=date(1990, 1, 1),
            funcao="Instrutor",
            salario=3000.00,
            carga_horaria=40,
            login="funcionario1",
            senha="senha123"
        )

        # Cria serviço
        self.servico = Servico.objects.create(
            modalidade="Pilates",
            niveis_dificuldade="Iniciante",
            descricao="Aula de Pilates para iniciantes"
        )

        # Cria aula
        self.aula = Aula.objects.create(
            data=date.today(),
            horario=time(10, 0),
            funcionario=self.funcionario
        )
        self.aula.servicos.add(self.servico)

        # Cria alunos
        self.aluno1 = Aluno.objects.create(
            cpf="11111111111",
            nome="Aluno Um",
            data_nascimento=date(2000, 1, 1),
            profissao="Estudante",
            historico_saude="Sem restrições",
            data_inicio_plano=date.today(),
            data_vencimento_plano=date.today(),
            plano_ativo=True
        )
        self.aluno2 = Aluno.objects.create(
            cpf="22222222222",
            nome="Aluno Dois",
            data_nascimento=date(1995, 5, 5),
            profissao="Professor",
            historico_saude="Sem restrições",
            data_inicio_plano=date.today(),
            data_vencimento_plano=date.today(),
            plano_ativo=True
        )

        # Cria horário disponível
        self.horario = HorarioDisponivel.objects.create(
            data=date.today(),
            horario_inicio=time(10, 0),
            capacidade_maxima=10,
            servico=self.servico,
            funcionario=self.funcionario
        )

        # Cria agendamentos para alunos (isso deve disparar signal e criar AulaAluno)
        self.agendamento1 = Agendamento.objects.create(
            horario_disponivel=self.horario,
            aluno=self.aluno1,
            cancelado=False
        )
        self.agendamento2 = Agendamento.objects.create(
            horario_disponivel=self.horario,
            aluno=self.aluno2,
            cancelado=False
        )

    def test_aula_str(self):
        self.assertIn("Aula", str(self.aula))
        self.assertIn(str(self.aula.codigo), str(self.aula))

    def test_aula_cancelar(self):
        self.aula.cancelar()
        self.assertTrue(self.aula.cancelada)

    def test_participacoes_criadas_automaticamente_via_signal(self):
        participacoes = AulaAluno.objects.filter(aula=self.aula)
        # Deveria existir participação para cada agendamento não cancelado
        alunos_participando = [p.aluno for p in participacoes]
        self.assertIn(self.aluno1, alunos_participando)
        self.assertIn(self.aluno2, alunos_participando)
        self.assertEqual(participacoes.count(), 2)

    def test_total_presentes_e_ausentes(self):
        participacao_aluno1 = AulaAluno.objects.get(aula=self.aula, aluno=self.aluno1)
        participacao_aluno2 = AulaAluno.objects.get(aula=self.aula, aluno=self.aluno2)

        participacao_aluno1.marcar_presenca()
        participacao_aluno2.marcar_ausencia()

        self.assertEqual(self.aula.total_presentes(), 1)
        self.assertEqual(self.aula.total_ausentes(), 1)

    def test_lista_alunos(self):
        alunos_lista = self.aula.lista_alunos()
        self.assertIn(self.aluno1, alunos_lista)
        self.assertIn(self.aluno2, alunos_lista)

    def test_aula_aluno_str_e_status_presenca(self):
        participacao = AulaAluno.objects.get(aula=self.aula, aluno=self.aluno1)
        self.assertIn(str(self.aluno1.nome), str(participacao))
        self.assertIn("Aula", str(participacao))
        self.assertIn("Ausente", participacao.status_presenca())

        participacao.marcar_presenca()
        self.assertIn("Presente", participacao.status_presenca())