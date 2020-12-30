from django.db import models


# Create your models here.

class Pergunta(models.Model):
    enunciado = models.TextField()
    alternativa_correta = models.IntegerField(choices=[
        (0, 'A'),
        (1, 'B'),
        (2, 'C'),
        (3, 'D')
    ])
    alternativas = models.JSONField()
    disponivel = models.BooleanField(default=False)

    def conferir_resposta(self, resposta_indice: int):
        resposta_indice = int(resposta_indice)
        return resposta_indice == self.alternativa_correta

    def __str__(self):
        return self.enunciado


class Aluno(models.Model):
    nome = models.CharField(max_length=64)
    email = models.EmailField(unique=True)
    criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Resposta(models.Model):
    criacao = models.DateTimeField(auto_now_add=True)
    pontos = models.IntegerField()
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['aluno', 'pergunta'], name='resposta_unica')
        ]
