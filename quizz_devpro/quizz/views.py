from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from quizz_devpro.quizz.models import Pergunta


def index(request):
    return render(request, 'quizz/index.html')


def perguntas(request, indice: int):
    pergunta = Pergunta.objects.filter(disponivel=True).order_by('id')[indice - 1]
    contexto = {'indice': indice, 'pergunta': pergunta}
    return render(request, 'quizz/pergunta.html', contexto)


def classificacao(request):
    return render(request, 'quizz/classificacao.html')
