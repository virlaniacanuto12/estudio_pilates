from datetime import date, timedelta
from django.test import TestCase
from django.urls import reverse
from studio.models import Aluno, Plano


class AlunoViewsTestCase(TestCase):
    def setUp(self):
        self.plano = Plano.objects.create(
            codigo=1,
            nome="Plano Mensal",
            qtd_aulas=10,
            valor_aula=50.0,
            status=True,
            limite_vigencia='M'
        )
        self.aluno = Aluno.objects.create(
            cpf="12345678900",
            nome="Maria",
            data_nascimento=date(1990, 1, 1),
            profissao="Médica",
            historico_saude="Asma leve",
            data_inicio_plano=date.today(),
            data_vencimento_plano=date.today() + timedelta(days=30),
            plano=self.plano
        )

    def test_listar_alunos(self):
        response = self.client.get(reverse('studio:listar_alunos'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.aluno.nome)

    def test_cadastro_aluno_post_valido(self):
        dados = {
            'cpf': '99988877766',
            'nome': 'Carlos',
            'data_nascimento': '2000-01-01',
            'profissao': 'Ator',
            'historico_saude': 'Nada',
            'data_inicio_plano': '2024-01-01',
            'data_vencimento_plano': '2024-12-31',
            'plano': self.plano.pk  
        }
        response = self.client.post(reverse('studio:cadastrar_aluno'), data=dados)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Aluno.objects.count(), 2)

    def test_cadastro_aluno_post_invalido(self):
        dados = {
            'email': 'invalido@example.com',
            'data_nascimento': '2000-01-01',
            'plano': self.plano.pk 
        }
        response = self.client.post(reverse('studio:cadastrar_aluno'), data=dados)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'studio/aluno/cadastrar_aluno.html')

        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn('cpf', form.errors)
        self.assertIn('Este campo é obrigatório.', form.errors['cpf'])

        self.assertEqual(Aluno.objects.count(), 1) 

    def test_editar_aluno_post_valido(self):
        url = reverse('studio:editar_aluno', args=[self.aluno.id])
        dados = {
            'cpf': self.aluno.cpf,
            'nome': 'Maria Editada',
            'data_nascimento': self.aluno.data_nascimento,
            'profissao': self.aluno.profissao,
            'historico_saude': self.aluno.historico_saude,
            'data_inicio_plano': self.aluno.data_inicio_plano,
            'data_vencimento_plano': self.aluno.data_vencimento_plano,
            'plano': self.plano.pk
        }
        response = self.client.post(url, data=dados)
        self.assertEqual(response.status_code, 302)
        self.aluno.refresh_from_db()
        self.assertEqual(self.aluno.nome, 'Maria Editada')

    def test_editar_aluno_post_invalido(self):
        url = reverse('studio:editar_aluno', args=[self.aluno.id])
        dados = {
            'cpf': '',
            'nome': '',
            'data_nascimento': self.aluno.data_nascimento,
            'profissao': '',
            'historico_saude': '',
            'data_inicio_plano': self.aluno.data_inicio_plano,
            'data_vencimento_plano': self.aluno.data_vencimento_plano,
            'plano': self.plano.pk
        }
        response = self.client.post(url, data=dados)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'studio/aluno/editar_aluno.html')

        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn('cpf', form.errors)
        self.assertIn('Este campo é obrigatório.', form.errors['cpf'])

    def test_excluir_aluno(self):
        response = self.client.post(reverse('studio:excluir_aluno', args=[self.aluno.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Aluno.objects.count(), 0)
