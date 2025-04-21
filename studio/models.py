# studio/models.py
from django.db import models

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