from datetime import date, time
from django.test import TestCase
from studio.models import HorarioDisponivel, Servico, Funcionario, Aluno, Agendamento

class AgendamentoModelTestCase(TestCase):
    def setUp(self):
        self.servico = Servico.objects.create(
            modalidade="Pilates Solo",
            niveis_dificuldade="Iniciante"
        )

        self.funcionario = Funcionario.objects.create(
            cpf="12345678901",
            rg="1234567",
            nome="Fernanda Silva",
            telefone="83999999999",
            email="fernanda@example.com",
            data_nascimento="1990-01-01",
            funcao="Instrutora",
            salario=3000.00,
            carga_horaria=40.0,
            horarios_trabalho="[]",
            login="fernanda123",
            senha="senha123"
        )

        self.aluno = Aluno.objects.create(
            cpf="98765432100",
            nome="Carlos Teste",
            data_nascimento="1995-05-10",
            profissao="Estudante",
            historico_saude="Sem restrições",
            data_inicio_plano=date.today(),
            data_vencimento_plano=date.today(),
            plano=None  
        )

        self.horario = HorarioDisponivel.objects.create(
            data=date.today(),
            horario_inicio=time(10, 0),
            horario_fim=time(11, 0),
            capacidade_maxima=2,
            servico=self.servico,
            funcionario=self.funcionario
        )

    def test_criar_agendamento(self):
        agendamento = Agendamento.objects.create(
            horario_disponivel=self.horario,
            aluno=self.aluno
        )
        self.assertEqual(Agendamento.objects.count(), 1)
        self.assertFalse(agendamento.cancelado)
        self.assertIsNone(agendamento.motivo_cancelamento)

    def test_cancelar_agendamento(self):
        agendamento = Agendamento.objects.create(
            horario_disponivel=self.horario,
            aluno=self.aluno
        )
        agendamento.cancelar_agendamento(motivo="Imprevisto")
        agendamento.refresh_from_db()
        self.assertTrue(agendamento.cancelado)
        self.assertEqual(agendamento.motivo_cancelamento, "Imprevisto")

    def test_reativar_agendamento(self):
        agendamento = Agendamento.objects.create(
            horario_disponivel=self.horario,
            aluno=self.aluno,
            cancelado=True,
            motivo_cancelamento="Problema"
        )
        agendamento.reativar_agendamento()
        agendamento.refresh_from_db()
        self.assertFalse(agendamento.cancelado)
        self.assertIsNone(agendamento.motivo_cancelamento)

    def test_unicidade_de_horario_aluno(self):
        Agendamento.objects.create(horario_disponivel=self.horario, aluno=self.aluno)
        with self.assertRaises(Exception):
            Agendamento.objects.create(horario_disponivel=self.horario, aluno=self.aluno)

    def test_str_representation(self):
        agendamento = Agendamento.objects.create(horario_disponivel=self.horario, aluno=self.aluno)
        esperado = f"Agendamento de {self.aluno.nome} para {self.horario}"
        self.assertEqual(str(agendamento), esperado)

        agendamento.cancelar_agendamento()
        agendamento.refresh_from_db()
        self.assertIn("(Cancelado)", str(agendamento))
