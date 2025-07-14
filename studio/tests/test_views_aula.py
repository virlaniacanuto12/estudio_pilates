from datetime import date, time, timedelta
from django.test import TestCase
from django.urls import reverse
from studio.models import (
    Aula, AulaAluno, Aluno, Funcionario, Servico,
    HorarioDisponivel, Agendamento
)

TOMORROW = date.today() + timedelta(days=1)


class AulaViewsTestCase(TestCase):
    def setUp(self):
        self.func = Funcionario.objects.create(
            cpf="12345678900", nome="Instrutor", data_nascimento=date(1980, 1, 1),
            funcao="Instrutor", salario=2000, carga_horaria=40,
            login="instrutor1", senha="senha123"
        )
        self.servico = Servico.objects.create(
            modalidade="Pilates", niveis_dificuldade="Iniciante", descricao="Desc"
        )
        self.aula = Aula.objects.create(
            data=TOMORROW, horario=time(10, 0), funcionario=self.func
        )
        self.aula.servicos.add(self.servico)

        self.aluno = Aluno.objects.create(
            cpf="11111111111", nome="Aluno Teste",
            data_nascimento=date(1995, 5, 5), profissao="Estudante",
            historico_saude="Ok",
            data_inicio_plano=TOMORROW, data_vencimento_plano=TOMORROW + timedelta(days=30),
            plano_ativo=True
        )

        self.horario = HorarioDisponivel.objects.create(
            data=TOMORROW, horario_inicio=time(10, 0),
            capacidade_maxima=5, servico=self.servico, funcionario=self.func
        )
        Agendamento.objects.create(horario_disponivel=self.horario, aluno=self.aluno)

    def test_listar_sem_filtro(self):
        resp = self.client.get(reverse("studio:listar_aulas"))
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.aula, resp.context["aulas"])

    def test_listar_com_filtros(self):
        resp = self.client.get(reverse("studio:listar_aulas"),
                               {"data": TOMORROW, "horario": "10:00:00"})
        self.assertIn(self.aula, resp.context["aulas"])

    def test_detalhes(self):
        resp = self.client.get(reverse("studio:detalhes_aula", args=[self.aula.pk]))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context["aula"], self.aula)

    def test_frequencia_get(self):
        resp = self.client.get(reverse("studio:frequencia_aula", args=[self.aula.pk]))
        self.assertEqual(resp.status_code, 200)

    def test_frequencia_post_valido(self):
        aulaaluno = AulaAluno.objects.get(aula=self.aula, aluno=self.aluno)
        data = {
            "form-TOTAL_FORMS": "1",
            "form-INITIAL_FORMS": "1",
            "form-MIN_NUM_FORMS": "0",
            "form-MAX_NUM_FORMS": "1000",
            "form-0-id": aulaaluno.id,
            "form-0-aula": self.aula.pk,
            "form-0-aluno": self.aluno.pk,
            "form-0-frequencia": "on",
            "form-0-evolucao_na_aula": "Ótimo rendimento",
        }
        resp = self.client.post(reverse("studio:frequencia_aula", args=[self.aula.pk]),
                                data, follow=True)
        aulaaluno.refresh_from_db()
        self.assertTrue(aulaaluno.frequencia)
        self.assertEqual(aulaaluno.evolucao_na_aula, "Ótimo rendimento")
        self.assertContains(resp, "Frequência e evolução salvas com sucesso.")

    def test_cadastro_post_valido(self):
        data = {
            "data": TOMORROW,
            "horario": time(15, 0),
            "funcionario": self.func.pk,
            "servicos": [self.servico.pk],
        }
        resp = self.client.post(reverse("studio:cadastro_aula"), data, follow=True)
        self.assertTrue(Aula.objects.filter(horario=time(15, 0)).exists())
        self.assertContains(resp, "Aula cadastrada com sucesso.")

    def test_editar_aula_post_valido(self):
        data = {
            "data": TOMORROW,
            "horario": time(11, 0),
            "funcionario": self.func.pk,
            "servicos": [self.servico.pk],
        }
        resp = self.client.post(reverse("studio:editar_aula", args=[self.aula.pk]),
                                data, follow=True)
        self.aula.refresh_from_db()
        self.assertEqual(self.aula.horario, time(11, 0))
        self.assertContains(resp, "Aula atualizada com sucesso.")

    def test_cancelar_aula(self):
        resp = self.client.post(reverse("studio:cancelar_aula", args=[self.aula.codigo]),
                                follow=True)
        self.aula.refresh_from_db()
        self.assertTrue(self.aula.cancelada)
        self.assertContains(resp, "foi cancelada com sucesso.")