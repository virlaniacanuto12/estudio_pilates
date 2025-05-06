# studio/models.py
from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class Servico(models.Model):

    # Opções para niveis_dificuldade
    NIVEIS_DIFICULDADE_CHOICES = [
        ('Iniciante', 'Iniciante'),
        ('Intermediário', 'Intermediário'),
        ('Avançado', 'Avançado'),
    ]

    modalidade = models.CharField(max_length=50) # Not Null por padrão (null=False, blank=False)
    niveis_dificuldade = models.CharField(
        max_length=30,
        choices=NIVEIS_DIFICULDADE_CHOICES # Usando as choices definidas acima
        # blank=False, null=False por padrão, atendendo "Not Null"
    )
    descricao = models.TextField(blank=True, null=True) # Mantido como opcional

    def __str__(self):
        return f"{self.modalidade} ({self.niveis_dificuldade})" # Sugestão para melhorar o __str__

class Funcionario(models.Model):
    funcao = models.CharField(max_length=100)
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    carga_horaria = models.FloatField()
    horarios_trabalho = models.JSONField(default=list)  # Armazena um array de strings
    login = models.CharField(max_length=50, unique=True)
    senha_hash = models.CharField(max_length=128)
    permissoes = models.JSONField(default=list)  # Armazena um array de strings
    is_admin = models.BooleanField(default=False)
    ultimo_acesso = models.DateTimeField(null=True, blank=True)

    def autenticar(self, senha: str) -> bool:
        return check_password(senha, self.senha_hash)

    # Vai calcular a carga horária a partir da quantidade de horários no array, e dps multiplica pelos dias da semana, retornando a carga horária semanal.
    def gerar_carga_horaria(self, horarios_trabalho: list) -> int:
        return len(horarios_trabalho) * 5 
    
    # Altera a carga horária com base nas horas extras trabalhadas
    def alterar_carga_horaria(self, horas_extras: float = 0.0) -> float:
        self.carga_horaria += horas_extras
        self.save()  # Salva automaticamente no banco de dados
        return self.carga_horaria

    def save(self, *args, **kwargs):
        if not self.senha_hash.startswith('pbkdf2_sha256$'):
            self.senha_hash = make_password(self.senha_hash)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.login} ({self.funcao})"