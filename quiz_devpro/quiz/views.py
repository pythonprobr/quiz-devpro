from datetime import datetime

from django.db import IntegrityError
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.utils.timezone import now

from quiz_devpro.quiz.forms import AlunoForm
from quiz_devpro.quiz.models import Pergunta, Aluno, Resposta


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
            return render(request, 'quiz/index.html', contexto)

    return render(request, 'quiz/index.html')


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
    return render(request, 'quiz/pergunta.html', contexto)


def classificacao(request):
    if 'aluno_id' not in request.session:
        return redirect('/')
    aluno_id = request.session['aluno_id']
    pontos_dct = Resposta.objects.filter(aluno_id=aluno_id).aggregate(Sum('pontos'))
    pontos_do_aluno = pontos_dct['pontos__sum']
    alunos_com_mais_pontos = Resposta.objects.values('aluno').annotate(Sum('pontos')).filter(
        pontos__sum__gt=pontos_do_aluno).count()
    primeiros_alunos_do_ranking = list(
        Resposta.objects.values('aluno', 'aluno__nome').annotate(Sum('pontos')).order_by('-pontos__sum')[:5]
    )
    contexto = {
        'pontos': pontos_do_aluno,
        'posicao': alunos_com_mais_pontos + 1,
        'primeiros_alunos_do_ranking': primeiros_alunos_do_ranking
    }
    return render(request, 'quiz/classificacao.html', contexto)
