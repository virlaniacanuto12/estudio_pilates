from datetime import date, time, timedelta
from django.test import TestCase
from django.urls import reverse
from studio.models import Servico, Funcionario, HorarioDisponivel, Agendamento, Aluno, Plano
from django.contrib.messages import get_messages
from django.utils import timezone

class AgendamentoViewsTestCase(TestCase):
    def setUp(self):
        self.servico = Servico.objects.create(modalidade="Pilates", niveis_dificuldade="Iniciante")
        self.funcionario = Funcionario.objects.create(
            cpf="12345678900", rg="000",
            nome="João", telefone="00000000", email="joao@example.com",
            data_nascimento="1990-01-01", funcao="Instrutor",
            salario=1000, carga_horaria=20,
            horarios_trabalho="[]", login="joao", senha="123"
        )
        self.horario_disponivel = HorarioDisponivel.objects.create(
            data=date.today() + timedelta(days=7),
            horario_inicio=time(9, 0),
            horario_fim=time(10, 0),
            capacidade_maxima=2,
            servico=self.servico,
            funcionario=self.funcionario
        )
        
        self.plano = Plano.objects.create(
            codigo=1,
            nome="Plano Mensal Teste",
            qtd_aulas=8,
            valor_aula=25.00,
            status=True,
            limite_vigencia='M'
        )

        self.aluno = Aluno.objects.create(
            cpf="00011122233", rg="111",
            nome="Maria", telefone="11111111", email="maria@example.com",
            data_nascimento=date(1995, 5, 5),
            status=True,
            profissao="Estudante",
            historico_saude="Nenhum problema",
            data_inicio_plano=date.today(),
            data_vencimento_plano=date.today() + timedelta(days=30),
            plano=self.plano
        )
        self.aluno2 = Aluno.objects.create(
            cpf="99988877766", rg="222",
            nome="Pedro", telefone="22222222", email="pedro@example.com",
            data_nascimento=date(1998, 1, 1),
            status=True,
            profissao="Engenheiro",
            historico_saude="Leve dor nas costas",
            data_inicio_plano=date.today(),
            data_vencimento_plano=date.today() + timedelta(days=30),
            plano=self.plano
        )

        self.LISTAR_AGENDAMENTOS_URL = reverse('studio:listar_agendamentos')
        self.LISTAR_HORARIOS_URL = reverse('studio:listar_horarios')

    def test_get_agendar_aluno(self):
        url = reverse('studio:agendar_aluno', args=[self.horario_disponivel.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'studio/agendamento/agendar_aluno.html')
        self.assertContains(response, f"Agendando para: {self.horario_disponivel.data.strftime('%d/%m/%Y')}")
        self.assertContains(response, self.aluno.nome)

    def test_post_agendar_aluno_valido(self):
        url = reverse('studio:agendar_aluno', args=[self.horario_disponivel.id])
        data = {
            'aluno_id': self.aluno.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.LISTAR_HORARIOS_URL) 
        
        self.assertTrue(Agendamento.objects.filter(
            horario_disponivel=self.horario_disponivel,
            aluno=self.aluno,
            cancelado=False
        ).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), f'Aluno {self.aluno.nome} agendado com sucesso para {self.horario_disponivel}.')

    def test_post_agendar_aluno_horario_cheio(self):
        Agendamento.objects.create(horario_disponivel=self.horario_disponivel, aluno=self.aluno)
        Agendamento.objects.create(horario_disponivel=self.horario_disponivel, aluno=self.aluno2)

        aluno3 = Aluno.objects.create(
            cpf="33344455566", rg="333",
            nome="Carlos", telefone="33333333", email="carlos@example.com",
            data_nascimento=date(1999, 1, 1), status=True,
            profissao="Programador", historico_saude="Nenhum",
            data_inicio_plano=date.today(), data_vencimento_plano=date.today() + timedelta(days=30),
            plano=self.plano
        )

        url = reverse('studio:agendar_aluno', args=[self.horario_disponivel.id])
        data = {
            'aluno_id': aluno3.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.LISTAR_HORARIOS_URL) 
        self.assertFalse(Agendamento.objects.filter(aluno=aluno3).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Este horário não possui mais vagas disponíveis. Vagas esgotadas.')


    def test_post_agendar_aluno_duplicado(self):
        Agendamento.objects.create(horario_disponivel=self.horario_disponivel, aluno=self.aluno)

        url = reverse('studio:agendar_aluno', args=[self.horario_disponivel.id])
        data = {
            'aluno_id': self.aluno.id 
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.LISTAR_HORARIOS_URL) 
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), f'Aluno {self.aluno.nome} já está agendado para {self.horario_disponivel}.')


    def test_post_agendar_aluno_sem_aluno(self):
        url = reverse('studio:agendar_aluno', args=[self.horario_disponivel.id])
        data = {
            'aluno_id': '' 
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.LISTAR_HORARIOS_URL) 
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Erro ao agendar: Field 'id' expected a number but got ''..")

    def test_get_listar_agendamentos(self):
        Agendamento.objects.create(horario_disponivel=self.horario_disponivel, aluno=self.aluno)
        outro_horario = HorarioDisponivel.objects.create(
            data=date.today() + timedelta(days=8),
            horario_inicio=time(14, 0),
            horario_fim=time(15, 0),
            capacidade_maxima=1,
            servico=self.servico,
            funcionario=self.funcionario
        )
        Agendamento.objects.create(horario_disponivel=outro_horario, aluno=self.aluno2)

        url = reverse('studio:listar_agendamentos')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.aluno.nome)
        self.assertContains(response, self.aluno2.nome)
        self.assertContains(response, self.servico.modalidade)
        self.assertTemplateUsed(response, 'studio/agendamento/listar_agendamentos.html')

    def test_get_editar_agendamento(self):
        agendamento = Agendamento.objects.create(
            horario_disponivel=self.horario_disponivel,
            aluno=self.aluno
        )
        url = reverse('studio:editar_agendamento', args=[agendamento.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="cancelado"') 
        self.assertTemplateUsed(response, 'studio/agendamento/editar_agendamento.html')

    def test_post_editar_agendamento_valido(self):
        agendamento = Agendamento.objects.create(
            horario_disponivel=self.horario_disponivel,
            aluno=self.aluno,
            cancelado=False
        )
        url = reverse('studio:editar_agendamento', args=[agendamento.id])
        data = {
            'horario_disponivel': self.horario_disponivel.id,
            'aluno': self.aluno.id, 
            'cancelado': 'on', 
            'motivo_cancelamento': 'Mudança de planos do aluno'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.LISTAR_AGENDAMENTOS_URL)
        agendamento.refresh_from_db()
        self.assertTrue(agendamento.cancelado)
        self.assertEqual(agendamento.motivo_cancelamento, 'Mudança de planos do aluno')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Agendamento atualizado com sucesso!')

    def test_post_editar_agendamento_invalido(self):
        agendamento = Agendamento.objects.create(
            horario_disponivel=self.horario_disponivel,
            aluno=self.aluno,
            cancelado=False
        )
        url = reverse('studio:editar_agendamento', args=[agendamento.id])
        data = {
            'horario_disponivel': self.horario_disponivel.id,
            'aluno': '', 
            'cancelado': False,
            'motivo_cancelamento': 'Teste de erro'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].errors)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Erro ao atualizar agendamento. Verifique os dados e tente novamente.')


    def test_get_excluir_agendamento(self):
        agendamento = Agendamento.objects.create(
            horario_disponivel=self.horario_disponivel,
            aluno=self.aluno,
            cancelado=False
        )
        url = reverse('studio:excluir_agendamento', args=[agendamento.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Você tem certeza que deseja cancelar o agendamento de:')
        self.assertTemplateUsed(response, 'studio/agendamento/excluir_agendamento.html')

    def test_post_excluir_agendamento_valido(self):
        agendamento = Agendamento.objects.create(
            horario_disponivel=self.horario_disponivel,
            aluno=self.aluno,
            cancelado=False
        )
        self.assertFalse(agendamento.cancelado)

        url = reverse('studio:excluir_agendamento', args=[agendamento.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.LISTAR_AGENDAMENTOS_URL)
        agendamento.refresh_from_db()
        self.assertTrue(agendamento.cancelado)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        expected_message = (
            f"Agendamento de {self.aluno.nome} em {agendamento.horario_disponivel} cancelado com sucesso. A vaga foi liberada."
        )
        self.assertEqual(str(messages[0]), expected_message)

    def test_post_excluir_agendamento_ja_cancelado(self):
        agendamento = Agendamento.objects.create(
            horario_disponivel=self.horario_disponivel,
            aluno=self.aluno,
            cancelado=True,
            motivo_cancelamento="Já cancelado"
        )
        url = reverse('studio:excluir_agendamento', args=[agendamento.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.LISTAR_AGENDAMENTOS_URL)
        agendamento.refresh_from_db()
        self.assertTrue(agendamento.cancelado)
        self.assertEqual(agendamento.motivo_cancelamento, "Já cancelado")
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Este agendamento já estava cancelado.')