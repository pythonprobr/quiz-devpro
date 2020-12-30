from django.forms import ModelForm

from quiz_devpro.quiz.models import Aluno


class AlunoForm(ModelForm):
    class Meta:
        model = Aluno
        fields = ['email', 'nome']
