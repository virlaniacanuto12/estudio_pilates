from datetime import date, time, timedelta
from django.test import TestCase
from django.urls import reverse
from studio.models import Servico, Funcionario, HorarioDisponivel, Agendamento, Aluno, Plano # Ensure Plano is imported if it exists
from django.contrib.messages import get_messages

class HorarioViewsTestCase(TestCase):
    def setUp(self):
        self.servico = Servico.objects.create(modalidade="Pilates", niveis_dificuldade="Iniciante")
        self.funcionario = Funcionario.objects.create(
            cpf="12345678900", rg="000",
            nome="João", telefone="00000000", email="joao@example.com",
            data_nascimento="1990-01-01", funcao="Instrutor",
            salario=1000, carga_horaria=20,
            horarios_trabalho="[]", login="joao", senha="123"
        )
        self.horario = HorarioDisponivel.objects.create(
            data=date.today() + timedelta(days=5),
            horario_inicio=time(10, 0),
            horario_fim=time(11, 0),
            capacidade_maxima=3, 
            servico=self.servico,
            funcionario=self.funcionario
        )
        self.LISTAR_HORARIOS_URL = reverse('studio:listar_horarios')


    def test_get_listar_horarios(self):
        url = reverse('studio:listar_horarios')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.servico.modalidade)
        self.assertTemplateUsed(response, 'studio/agendamento/listar_horarios.html')

    def test_get_cadastrar_horario(self):
        url = reverse('studio:cadastrar_horario_disponivel')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="data"')
        self.assertTemplateUsed(response, 'studio/agendamento/cadastrar_horario_disponivel.html')

    def test_post_cadastrar_horario_valido(self):
        url = reverse('studio:cadastrar_horario_disponivel')
        data = {
            'data': (date.today() + timedelta(days=1)).isoformat(),
            'horario_inicio': '08:00',
            'horario_fim': '09:00',
            'capacidade_maxima': 2, # Value is within 1-5 range
            'servico': self.servico.id,
            'funcionario': self.funcionario.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.LISTAR_HORARIOS_URL)
        self.assertTrue(HorarioDisponivel.objects.filter(
            data=(date.today() + timedelta(days=1)),
            horario_inicio=time(8, 0),
            horario_fim=time(9, 0),
            capacidade_maxima=2,
            servico=self.servico,
            funcionario=self.funcionario
        ).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Horário disponível cadastrado com sucesso!')

    def test_post_cadastrar_horario_invalido(self):
        url = reverse('studio:cadastrar_horario_disponivel')
        data = {
            'data': 'data_invalida', 
            'horario_inicio': '08:00',
            'horario_fim': '09:00',
            'capacidade_maxima': 'abc', 
            'servico': self.servico.id,
            'funcionario': self.funcionario.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200) # Should render page with errors
        self.assertFalse(HorarioDisponivel.objects.filter(horario_inicio=time(8,0)).exists())
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].errors)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Erro ao cadastrar horário. Verifique os dados e tente novamente.')


    def test_get_editar_horario(self):
        url = reverse('studio:editar_horario', args=[self.horario.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="data"')
        self.assertTemplateUsed(response, 'studio/agendamento/editar_horario.html')
        self.assertContains(response, self.horario.servico.modalidade)
        self.assertContains(response, self.horario.funcionario.nome)

    def test_post_editar_horario_valido(self):
        url = reverse('studio:editar_horario', args=[self.horario.id])
        novo_capacidade = 5 
        data = {
            'data': self.horario.data.isoformat(),
            'horario_inicio': self.horario.horario_inicio.strftime('%H:%M'),
            'horario_fim': self.horario.horario_fim.strftime('%H:%M'),
            'capacidade_maxima': novo_capacidade,
            'servico': self.servico.id,
            'funcionario': self.funcionario.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.LISTAR_HORARIOS_URL)
        self.horario.refresh_from_db()
        self.assertEqual(self.horario.capacidade_maxima, novo_capacidade)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Horário disponível atualizado com sucesso!')

    def test_post_editar_horario_invalido(self):
        url = reverse('studio:editar_horario', args=[self.horario.id])
        data = {
            'data': self.horario.data.isoformat(),
            'horario_inicio': 'horario_invalido', 
            'horario_fim': '11:00',
            'capacidade_maxima': self.horario.capacidade_maxima,
            'servico': self.servico.id,
            'funcionario': self.funcionario.id,
        }
        response = self.client.post(url, data)
        self.horario.refresh_from_db()
        self.assertNotEqual(self.horario.horario_inicio.strftime('%H:%M'), 'horario_invalido')
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].errors)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Erro ao atualizar horário. Verifique os dados e tente novamente.')

    def test_get_excluir_horario(self):
        url = reverse('studio:excluir_horario', args=[self.horario.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'studio/agendamento/excluir_horario.html')
        self.assertContains(response, f"Você tem certeza que deseja excluir permanentemente o horário:")


    def test_post_excluir_horario_sem_agendamento(self):
        url = reverse('studio:excluir_horario', args=[self.horario.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.LISTAR_HORARIOS_URL)
        self.assertFalse(HorarioDisponivel.objects.filter(id=self.horario.id).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Horário disponível excluído com sucesso!')

    def test_post_excluir_horario_com_agendamento_ativo(self):
        aluno = Aluno.objects.create(
            cpf="00011122233", rg="111",
            nome="Maria", telefone="11111111", email="maria@example.com",
            data_nascimento=date(1995, 5, 5), 
            status=True,
            profissao="Estudante", 
            historico_saude="Nenhum problema", 
            data_inicio_plano=date.today(), 
            data_vencimento_plano=date.today() + timedelta(days=30), 
        )
        Agendamento.objects.create(
            aluno=aluno,
            horario_disponivel=self.horario,
            data_agendamento=date.today(),
            cancelado=False
        )

        url = reverse('studio:excluir_horario', args=[self.horario.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.LISTAR_HORARIOS_URL)
        self.assertTrue(HorarioDisponivel.objects.filter(id=self.horario.id).exists()) 
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Não é possível excluir este horário porque existem agendamentos ativos vinculados a ele.')