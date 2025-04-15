from django.db import models

# Model para os Serviços oferecidos pelo estúdio
class Servico(models.Model):
    # Django cria um 'id' (PK) automaticamente, que serve como nosso 'cod'
    
    modalidade = models.CharField(max_length=50)
    nivel_dificuldade = models.CharField(max_length=50, blank=True, null=True) # Ex: "Iniciante", "Intermediário", "Avançado". Opcional?
    descricao = models.TextField(blank=True, null=True) # Descrição mais detalhada do serviço (opcional)

    # Define como o objeto Servico será exibido (ex: na área admin)
    def __str__(self):
        return self.modalidade
