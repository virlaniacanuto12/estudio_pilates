from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Agendamento, Aula, AulaAluno

@receiver(post_save, sender=Agendamento)
def criar_participacao(sender, instance, created, **kwargs):
    aula = Aula.objects.filter(data=instance.data, horario=instance.horario).first()
    if aula:
        AulaAluno.objects.get_or_create(aula=aula, aluno=instance.aluno)

@receiver(post_delete, sender=Agendamento)
def remover_participacao(sender, instance, **kwargs):
    aula = Aula.objects.filter(data=instance.data, horario=instance.horario).first()
    if aula:
        AulaAluno.objects.filter(aula=aula, aluno=instance.aluno).delete()