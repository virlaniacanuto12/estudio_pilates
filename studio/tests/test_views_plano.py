from django.test import TestCase
from django.urls import reverse
from studio.models import Plano


class PlanoViewsTestCase(TestCase):
    def setUp(self):
        self.plano = Plano.objects.create(
            codigo=1,
            nome="Plano Inicial",
            qtd_aulas=10,
            valor_aula=45.0,
            status=True,
            limite_vigencia='M'
        )

    def test_listar_planos(self):
        response = self.client.get(reverse('studio:listar_planos'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.plano.nome)

    def test_cadastro_plano_post_valido(self):
        dados = {
            'codigo': 2,
            'nome': 'Plano Avançado',
            'qtd_aulas': 15,
            'valor_aula': 60.0,
            'status': True,
            'limite_vigencia': 'S'
        }
        response = self.client.post(reverse('studio:cadastrar_plano'), data=dados)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Plano.objects.count(), 2)

    def test_cadastro_plano_post_invalido(self):
        dados = {
            'valor_aula': 40.0,
            'qtd_aulas': 10,
            'limite_vigencia': 'M',
        }
        response = self.client.post(reverse('studio:cadastrar_plano'), data=dados)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'studio/plano/cadastrar_plano.html')
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn('codigo', form.errors)
        self.assertIn('nome', form.errors)
        self.assertIn('Este campo é obrigatório.', form.errors['codigo'])
        self.assertIn('Este campo é obrigatório.', form.errors['nome'])

    def test_editar_plano_post_valido(self):
        dados = {
            'codigo': self.plano.codigo,
            'nome': 'Plano Atualizado',
            'qtd_aulas': 20,
            'valor_aula': 50.0,
            'status': True,
            'limite_vigencia': 'T'
        }
        response = self.client.post(reverse('studio:editar_plano', args=[self.plano.codigo]), data=dados)
        self.assertEqual(response.status_code, 302)
        self.plano.refresh_from_db()
        self.assertEqual(self.plano.nome, 'Plano Atualizado')

    def test_editar_plano_post_invalido(self):
        dados = {
            'codigo': self.plano.codigo,
            'nome': '',
            'qtd_aulas': '',
            'valor_aula': '',
            'limite_vigencia': '',
            'status': False
        }
        response = self.client.post(reverse('studio:editar_plano', args=[self.plano.codigo]), data=dados)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'studio/plano/editar_plano.html') 
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn('nome', form.errors)
        self.assertIn('Este campo é obrigatório.', form.errors['nome'])

    def test_excluir_plano(self):
        response = self.client.post(reverse('studio:excluir_plano', args=[self.plano.codigo]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Plano.objects.count(), 0)
