from datetime import date, time
from django.test import TestCase
from studio.models import HorarioDisponivel, Servico, Funcionario, Aluno, Agendamento

class HorarioDisponivelModelTestCase(TestCase):
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
            plano=None  # ou algum plano se for obrigatório
        )

        self.horario = HorarioDisponivel.objects.create(
            data=date.today(),
            horario_inicio=time(10, 0),
            horario_fim=time(11, 0),
            capacidade_maxima=2,
            servico=self.servico,
            funcionario=self.funcionario
        )

    def test_criacao_valida_de_horario(self):
        self.assertEqual(HorarioDisponivel.objects.count(), 1)
        self.assertEqual(self.horario.vagas_disponiveis, 2)
        self.assertFalse(self.horario.esta_cheio)

    def test_str_horario_formatado(self):
        esperado = f"{self.horario.data.strftime('%d/%m/%Y')} às {self.horario.horario_inicio.strftime('%H:%M')}({self.servico.modalidade}) com {self.funcionario.nome}"
        self.assertEqual(str(self.horario), esperado)

    def test_vagas_disponiveis_e_esta_cheio(self):
        Agendamento.objects.create(horario_disponivel=self.horario, aluno=self.aluno, cancelado=False)
        outro_aluno = Aluno.objects.create(
            cpf="12312312312",
            nome="Outro Aluno",
            data_nascimento="1990-10-10",
            profissao="Professor",
            historico_saude="N/A",
            data_inicio_plano=date.today(),
            data_vencimento_plano=date.today(),
            plano=None
        )
        Agendamento.objects.create(horario_disponivel=self.horario, aluno=outro_aluno, cancelado=False)

        self.horario.refresh_from_db()
        self.assertEqual(self.horario.vagas_disponiveis, 0)
        self.assertTrue(self.horario.esta_cheio)

    def test_unicidade_de_data_horario_servico(self):
        with self.assertRaises(Exception):  # IntegrityError se quiser especificar
            HorarioDisponivel.objects.create(
                data=self.horario.data,
                horario_inicio=self.horario.horario_inicio,
                servico=self.servico
            )
