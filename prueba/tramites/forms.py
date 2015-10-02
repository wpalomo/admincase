from django import forms
from .models import Tramite
from .models import RequisitosPresentados

class RequisitoForm(forms.ModelForm):

    class Meta:
        model = RequisitosPresentados
        fields = '__all__'