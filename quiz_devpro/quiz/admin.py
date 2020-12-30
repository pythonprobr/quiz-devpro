from django.contrib import admin

# Register your models here.
from quiz_devpro.quiz.models import Pergunta, Aluno, Resposta


@admin.register(Pergunta)
class PerguntaAdmin(admin.ModelAdmin):
    list_display = ('id', 'enunciado', 'disponivel')


@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('email', 'nome', 'criacao')


@admin.register(Resposta)
class RespostaAdmin(admin.ModelAdmin):
    list_display = ('criacao', 'pergunta', 'aluno', 'pontos')
