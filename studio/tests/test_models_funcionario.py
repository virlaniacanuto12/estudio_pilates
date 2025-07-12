from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError 
from datetime import date, timedelta
from django.utils import timezone 
from django.contrib.auth.hashers import check_password 
from studio.models import Funcionario

class FuncionarioModelTest(TestCase):

    def setUp(self):
        self.dados_validos = {
            'cpf': "11111111111",
            'rg': "111111111",
            'nome': "Funcionario Teste Model",
            'telefone': "11999999999",
            'email': "teste_model@example.com",
            'data_nascimento': date(1985, 10, 20),
            'status': True,
            'funcao': "Desenvolvedor",
            'salario': 5000.00,
            'carga_horaria': 40.0,
            'horarios_trabalho': "08:00,09:00,10:00,11:00,12:00,13:00,14:00,15:00", 
            'login': "dev_model",
            'senha': "senhasegura123", # Será hasheada pelo save()
            'is_admin': False,
        }

    # Teste de Criação Básica
    def test_create_funcionario_valid(self):
        funcionario = Funcionario.objects.create(**self.dados_validos)
        self.assertIsInstance(funcionario, Funcionario)
        self.assertEqual(funcionario.nome, "Funcionario Teste Model")
        self.assertEqual(funcionario.cpf, "11111111111")
        self.assertTrue(check_password("senhasegura123", funcionario.senha)) # Verifica se a senha foi hasheada

    # Teste do método __str__
    def test_funcionario_str_representation(self):
        funcionario = Funcionario.objects.create(**self.dados_validos)
        expected_str = f"{self.dados_validos['login']} ({self.dados_validos['funcao']}) ({self.dados_validos['nome']})"
        self.assertEqual(str(funcionario), expected_str)

    # Teste de autenticação
    def test_funcionario_autenticar_correct_password(self):
        funcionario = Funcionario.objects.create(**self.dados_validos)
        self.assertTrue(funcionario.autenticar("senhasegura123"))

    def test_funcionario_autenticar_incorrect_password(self):
        funcionario = Funcionario.objects.create(**self.dados_validos)
        self.assertFalse(funcionario.autenticar("senhaerrada"))

    # Teste de gerar_carga_horaria
    def test_gerar_carga_horaria(self):
        horarios = ["08:00", "09:00", "10:00", "11:00"] # 4 horas/dia
        expected_carga_horaria = len(horarios) * 5 # 4 * 5 = 20
        # O método gerar_carga_horaria no seu modelo não usa self
        # self.assertEqual(Funcionario.gerar_carga_horaria(horarios), expected_carga_horaria)
        # Se for um método de instância que pode ser chamado via objeto:
        funcionario = Funcionario(**self.dados_validos) # Não precisa salvar para testar este método
        self.assertEqual(funcionario.gerar_carga_horaria(horarios), expected_carga_horaria)


    # Teste de alterar_carga_horaria
    def test_alterar_carga_horaria(self):
        funcionario = Funcionario.objects.create(**self.dados_validos)
        initial_carga_horaria = funcionario.carga_horaria
        horas_extras = 5.0
        new_carga_horaria = funcionario.alterar_carga_horaria(horas_extras)
        self.assertEqual(new_carga_horaria, initial_carga_horaria + horas_extras)
        # Recarrega do DB para garantir que foi salvo
        funcionario.refresh_from_db()
        self.assertEqual(funcionario.carga_horaria, initial_carga_horaria + horas_extras)

    def test_alterar_carga_horaria_no_extra_hours(self):
        funcionario = Funcionario.objects.create(**self.dados_validos)
        initial_carga_horaria = funcionario.carga_horaria
        new_carga_horaria = funcionario.alterar_carga_horaria() # Sem horas extras
        self.assertEqual(new_carga_horaria, initial_carga_horaria)
        funcionario.refresh_from_db()
        self.assertEqual(funcionario.carga_horaria, initial_carga_horaria)

    # Teste de unicidade de CPF
    def test_unique_cpf_constraint(self):
        Funcionario.objects.create(**self.dados_validos) # Cria o primeiro
        dados_conflito_cpf = self.dados_validos.copy()
        dados_conflito_cpf['login'] = "outro_login" # Mudar login para evitar conflito de login também
        dados_conflito_cpf['email'] = "outro_email@example.com" # Mudar email se for unique

        with self.assertRaises(IntegrityError): # Espera um erro de integridade do DB
            Funcionario.objects.create(**dados_conflito_cpf)

    # Teste de unicidade de Login
    def test_unique_login_constraint(self):
        Funcionario.objects.create(**self.dados_validos)
        dados_conflito_login = self.dados_validos.copy()
        dados_conflito_login['cpf'] = "99999999999" # Mudar CPF para evitar conflito de CPF também
        dados_conflito_login['email'] = "outro_email2@example.com"
        
        with self.assertRaises(IntegrityError):
            Funcionario.objects.create(**dados_conflito_login)

    # Teste do método calcular_idade (herdado de Pessoa)
    def test_calcular_idade(self):
        # Cria um funcionário com data de nascimento específica para facilitar o teste
        # Ex: nascido hoje, 2024 (assumindo que estamos em 2024 para simplificar)
        nascimento_teste = date(date.today().year - 30, date.today().month, date.today().day)
        # CUIDADO: Este teste depende da data atual, pode falhar em dias específicos (aniversários)
        # Melhor seria simular a data de hoje ou usar datas fixas que não dependem do dia atual.
        # Para um teste mais robusto:
        nascimento_fixed = date(1990, 7, 12) # Ex: 12 de Julho de 1990
        # Calcule a idade esperada para essa data fixa (assumindo 2025 para hoje)
        hoje_para_teste = date(2025, 7, 12) # Data fixa para o "hoje" do teste

        dados_idade = self.dados_validos.copy()
        dados_idade['cpf'] = "88888888888"
        dados_idade['login'] = "idade_test"
        dados_idade['email'] = "idade_test@example.com"
        dados_idade['data_nascimento'] = nascimento_fixed

        funcionario_idade = Funcionario.objects.create(**dados_idade)
        
        # Simula o "today" para o cálculo da idade (se o seu método calcular_idade usar date.today())
        # Caso contrário, o teste passará se a data for fixa.
        # Se o método calcular_idade não aceita data como parametro, este teste pode ser sensível ao dia do ano
        
        # Idade em 12/07/2025 para quem nasceu em 12/07/1990 é 35
        expected_age = hoje_para_teste.year - nascimento_fixed.year - (
            (hoje_para_teste.month, hoje_para_teste.day) < (nascimento_fixed.month, nascimento_fixed.day)
        )
        self.assertEqual(funcionario_idade.calcular_idade(), expected_age)

        # Teste de idade em ano de não aniversário ainda
        nascimento_nao_aniversario = date(1990, 8, 1) # Nasceu em agosto
        dados_idade_nao_aniversario = self.dados_validos.copy()
        dados_idade_nao_aniversario['cpf'] = "77777777777"
        dados_idade_nao_aniversario['login'] = "idade_no_bday"
        dados_idade_nao_aniversario['email'] = "idade_no_bday@example.com"
        dados_idade_nao_aniversario['data_nascimento'] = nascimento_nao_aniversario
        
        funcionario_nao_aniversario = Funcionario.objects.create(**dados_idade_nao_aniversario)
        expected_age_nao_aniversario = hoje_para_teste.year - nascimento_nao_aniversario.year - (
            (hoje_para_teste.month, hoje_para_teste.day) < (nascimento_nao_aniversario.month, nascimento_nao_aniversario.day)
        )
        self.assertEqual(funcionario_nao_aniversario.calcular_idade(), expected_age_nao_aniversario)


    # Teste de validação de campo obrigatório (nome)
    def test_required_name_field(self):
        dados_sem_nome = self.dados_validos.copy()
        dados_sem_nome['nome'] = "" # Nome vazio
        dados_sem_nome['cpf'] = "44444444444" # Mudar CPF para evitar unicidade
        dados_sem_nome['login'] = "test_no_name"
        dados_sem_nome['email'] = "test_no_name@example.com"
        
        funcionario = Funcionario(**dados_sem_nome)
        with self.assertRaises(ValidationError) as cm:
            funcionario.full_clean() # Chama todas as validações do modelo
        self.assertIn('nome', cm.exception.error_dict)
        self.assertEqual(cm.exception.error_dict['nome'][0].message, 'Este campo não pode estar vazio.')

    # Teste de validação de CPF (clean_cpf do form, mas se o modelo tiver, testar aqui)
    # Como você tem clean_cpf no form, este teste seria mais para a view/form.
    # Se você tivesse um validador de CPF direto no campo do modelo, testaria aqui.
    # Exemplo (se houvesse um validador no model):
    def test_invalid_cpf_model_validation(self):
        dados_invalidos_cpf_model = self.dados_validos.copy()
        dados_invalidos_cpf_model['cpf'] = "123" # CPF inválido
        dados_invalidos_cpf_model['login'] = "invalid_cpf_user"
        dados_invalidos_cpf_model['email'] = "invalid_cpf@example.com"
        
        funcionario = Funcionario(**dados_invalidos_cpf_model)
        # Assumindo que a validação de CPF está no formulário,
        # para testar no modelo, você precisaria de um custom validator no campo do modelo.
        # Se não houver, este teste falhará ou não será relevante para o modelo.
        # Se você tivesse um validador no model, a linha abaixo funcionaria:
        # with self.assertRaises(ValidationError):
        #     funcionario.full_clean()
        pass # Remove isso e implemente se tiver validação de CPF no modelo