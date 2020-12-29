from django.contrib import admin

# Register your models here.
from quizz_devpro.quizz.models import Pergunta, Aluno


@admin.register(Pergunta)
class PerguntaAdmin(admin.ModelAdmin):
    list_display = ('id', 'enunciado', 'disponivel')


@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('email', 'nome', 'criacao')
