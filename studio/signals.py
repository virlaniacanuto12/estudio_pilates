from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Agendamento, Aula, AulaAluno

@receiver(post_save, sender=Agendamento)
def sincronizar_participacao_agendamento(sender, instance, created, **kwargs):
    aula = Aula.objects.filter(
        data=instance.horario_disponivel.data,
        horario=instance.horario_disponivel.horario_inicio
    ).first()

    if not aula:
        return

    if created or not instance.cancelado:
        # Se for criado ou "descancelado", cria participação
        AulaAluno.objects.get_or_create(aula=aula, aluno=instance.aluno)
    elif instance.cancelado:
        # Se for um cancelamento (por edição), remove a participação
        AulaAluno.objects.filter(aula=aula, aluno=instance.aluno).delete()

@receiver(post_delete, sender=Agendamento)
def remover_participacao_agendamento(sender, instance, **kwargs):
    aula = Aula.objects.filter(
        data=instance.horario_disponivel.data,
        horario=instance.horario_disponivel.horario_inicio
    ).first()

    if aula:
        AulaAluno.objects.filter(aula=aula, aluno=instance.aluno).delete()
