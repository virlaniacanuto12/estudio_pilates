from datetime import date, time
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from studio.models import Aula, AulaAluno, Aluno, Funcionario, Servico, HorarioDisponivel, Agendamento

class AulaViewsTestCase(TestCase):
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
        self.servico = Servico.objects.create(
            modalidade="Pilates",
            niveis_dificuldade="Iniciante",
            descricao="Descricao teste"
        )
        self.aula = Aula.objects.create(
            data=date.today(),
            horario=time(10, 0),
            funcionario=self.funcionario
        )
        self.aula.servicos.add(self.servico)

        self.aluno = Aluno.objects.create(
            cpf="11111111111",
            nome="Aluno Teste",
            data_nascimento=date(1995, 5, 5),
            profissao="Estudante",
            historico_saude="Sem restrições",
            data_inicio_plano=date.today(),
            data_vencimento_plano=date.today(),
            plano_ativo=True
        )

        self.horario = HorarioDisponivel.objects.create(
            data=date.today(),
            horario_inicio=time(10, 0),
            capacidade_maxima=5,
            servico=self.servico,
            funcionario=self.funcionario
        )

        self.agendamento = Agendamento.objects.create(
            horario_disponivel=self.horario,
            aluno=self.aluno,
            cancelado=False
        )

    def test_listar_aulas_sem_filtros(self):
        url = reverse('studio:listar_aulas')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.aula, response.context['aulas'])

    def test_listar_aulas_com_data(self):
        url = reverse('studio:listar_aulas')
        response = self.client.get(url, {'data': self.aula.data})
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.aula, response.context['aulas'])

    def test_listar_aulas_com_data_e_horario(self):
        url = reverse('studio:listar_aulas')
        response = self.client.get(url, {'data': self.aula.data, 'horario': self.aula.horario.strftime("%H:%M:%S")})
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.aula, response.context['aulas'])

    def test_listar_aulas_somente_horario_retorna_vazio_e_warning(self):
        url = reverse('studio:listar_aulas')
        response = self.client.get(url, {'horario': self.aula.horario.strftime("%H:%M:%S")}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Para filtrar por horário, você deve informar a data.")
        self.assertEqual(len(response.context['aulas']), 0)

    def test_detalhes_aula(self):
        url = reverse('studio:detalhes_aula', args=[self.aula.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['aula'], self.aula)
        self.assertTrue('participacoes' in response.context)

    def test_frequencia_aula_get(self):
        url = reverse('studio:frequencia_aula', args=[self.aula.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('formset', response.context)
        self.assertEqual(response.context['aula'], self.aula)

    def test_frequencia_aula_post_valido(self):
        url = reverse('studio:frequencia_aula', args=[self.aula.pk])
        aulaaluno = AulaAluno.objects.get(aula=self.aula, aluno=self.aluno)
        data = {
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '1',
            'form-MIN_NUM_FORMS': '0',
            'form-MAX_NUM_FORMS': '1000',
            'form-0-id': aulaaluno.id,
            'form-0-frequencia': 'on',         
            'form-0-evolucao_na_aula': 'Evolução testada'
        }
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        aulaaluno.refresh_from_db()
        self.assertTrue(aulaaluno.frequencia)                       
        self.assertEqual(aulaaluno.evolucao_na_aula, 'Evolução testada')
        self.assertContains(response, "Frequência e evolução salvas com sucesso.")

    def test_cadastro_aula_get(self):
        url = reverse('studio:cadastro_aula')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)

    def test_cadastro_aula_post_valido(self):
        url = reverse('studio:cadastro_aula')
        data = {
            'data': date.today(),
            'horario': time(17, 0),
            'funcionario': self.funcionario.pk,
            'servicos': [self.servico.pk]
        }
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Aula.objects.filter(horario=time(17, 0)).exists())
        self.assertContains(response, "Aula cadastrada com sucesso.")

    def test_editar_aula_get(self):
        url = reverse('studio:editar_aula', args=[self.aula.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertEqual(response.context['aula'], self.aula)

    def test_editar_aula_post_valido(self):
        url = reverse('studio:editar_aula', args=[self.aula.pk])
        data = {
            'data': date.today(),
            'horario': time(20, 0),
            'funcionario': self.funcionario.pk,
            'servicos': [self.servico.pk]
        }
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.aula.refresh_from_db()
        self.assertEqual(self.aula.horario.hour, 20)
        self.assertContains(response, "Aula atualizada com sucesso.")

    def test_editar_aula_cancelada_redireciona(self):
        self.aula.cancelar()
        url = reverse('studio:editar_aula', args=[self.aula.pk])
        response = self.client.get(url, follow=True)
        self.assertContains(response, "Não é possível editar uma aula cancelada.")

    def test_cancelar_aula(self):
        url = reverse('studio:cancelar_aula', args=[self.aula.codigo])
        response = self.client.post(url, follow=True)
        self.aula.refresh_from_db()
        self.assertTrue(self.aula.cancelada)
        self.assertContains(response, f'Aula {self.aula.codigo} foi cancelada com sucesso.')