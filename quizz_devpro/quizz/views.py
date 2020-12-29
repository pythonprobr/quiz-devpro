from datetime import datetime

from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.utils.timezone import now

from quizz_devpro.quizz.forms import AlunoForm
from quizz_devpro.quizz.models import Pergunta, Aluno, Resposta


def index(request):
    if request.method == 'POST':
        email = email = request.POST['email']
        if Aluno.objects.filter(email=email):
            aluno = Aluno.objects.get(email=email)
            request.session['aluno_id'] = aluno.id
            return redirect('/perguntas/1')
        # Salvando o aluno
        form = AlunoForm(request.POST)
        if form.is_valid():
            aluno = form.save()
            request.session['aluno_id'] = aluno.id
            return redirect('/perguntas/1')
        else:
            contexto = {'form': form}
            return render(request, 'quizz/index.html', contexto)

    return render(request, 'quizz/index.html')


def perguntas(request, indice: int):
    if 'aluno_id' not in request.session:
        return redirect('/')
    aluno_id = request.session['aluno_id']
    try:
        pergunta = Pergunta.objects.filter(disponivel=True).order_by('id')[indice - 1]
    except IndexError:
        return redirect('/classificacao')
    if request.method == 'POST':
        resposta_indice = int(request.POST['resposta_indice'])
        resposta_correta = pergunta.conferir_resposta(resposta_indice)
        if resposta_correta:
            try:
                resposta = Resposta.objects.filter(pergunta=pergunta).order_by('criacao')[0]
            except IndexError:
                pontos = 100
            else:
                tempo_primeira_resposta = resposta.criacao
                diferenca = now() - tempo_primeira_resposta
                pontos = max(100 - int(diferenca.total_seconds()), 0)
            try:
                Resposta.objects.create(pontos=pontos, aluno_id=aluno_id, pergunta=pergunta)
            except IntegrityError:
                pass
            return redirect(f'/perguntas/{indice + 1}')

        else:
            contexto = {'indice': indice, 'pergunta': pergunta, 'resposta_indice': resposta_indice}
    else:
        contexto = {'indice': indice, 'pergunta': pergunta}
    return render(request, 'quizz/pergunta.html', contexto)


def classificacao(request):
    if 'aluno_id' not in request.session:
        return redirect('/')
    return render(request, 'quizz/classificacao.html')
