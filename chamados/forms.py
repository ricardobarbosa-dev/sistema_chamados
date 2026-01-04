from django import forms
from .models import RespostaChamado

class RespostaChamadoForm(forms.ModelForm):
    class Meta:
        model = RespostaChamado
        fields = ['mensagem']
