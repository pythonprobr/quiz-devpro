from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from quizz_devpro.quizz.forms import AlunoForm
from quizz_devpro.quizz.models import Pergunta, Aluno


def index(request):
    if request.method == 'POST':
        email = email = request.POST['email']
        if Aluno.objects.filter(email=email).exists():
            request.session['email'] = email
            return redirect('/perguntas/1')
        # Salvando o aluno
        form = AlunoForm(request.POST)
        if form.is_valid():
            form.save()
            request.session['email'] = email
            return redirect('/perguntas/1')
        else:
            contexto = {'form': form}
            return render(request, 'quizz/index.html', contexto)

    return render(request, 'quizz/index.html')


def perguntas(request, indice: int):
    if 'email' not in request.session:
        return redirect('/')
    pergunta = Pergunta.objects.filter(disponivel=True).order_by('id')[indice - 1]
    contexto = {'indice': indice, 'pergunta': pergunta}
    return render(request, 'quizz/pergunta.html', contexto)


def classificacao(request):
    if 'email' not in request.session:
        return redirect('/')
    return render(request, 'quizz/classificacao.html')
