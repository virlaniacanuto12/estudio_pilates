from django.test import TestCase
from studio.models import Plano


class PlanoModelTestCase(TestCase):
    def setUp(self):
        self.plano = Plano.objects.create(
            codigo=1,
            nome="Plano Mensal",
            qtd_aulas=8,
            valor_aula=40.0,
            status=True,
            limite_vigencia='M'
        )

    def test_criacao_plano(self):
        self.assertEqual(self.plano.nome, "Plano Mensal")
        self.assertEqual(self.plano.qtd_aulas, 8)

    def test_str(self):
        self.assertEqual(str(self.plano), "Plano Mensal (Código: 1)")
