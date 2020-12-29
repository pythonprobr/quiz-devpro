from django.forms import ModelForm

from quizz_devpro.quizz.models import Aluno


class AlunoForm(ModelForm):
    class Meta:
        model = Aluno
        fields = ['email', 'nome']
