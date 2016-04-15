from django import forms
from django.contrib.auth.models import User

from .models import TipoNota, Nota


class NotaForm(forms.ModelForm):

    tipo_nota = forms.ModelChoiceField(required=True,
                                       queryset=TipoNota.objects.all(),
                                       widget=forms.Select(attrs=(
                                           {'class': 'form-control'})))
    descripcion = forms.CharField(required=True, max_length=3000,
                                  widget=forms.Textarea(attrs=({
                                      'class': 'form-control'})))
    usuario = forms.ModelChoiceField(required=False, queryset=User.objects.all())

    class Meta:
        model = Nota
        fields = ['tipo_nota', 'descripcion', 'usuario']
