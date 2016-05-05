from django import forms

from .models import Entidad


class EntidadForm(forms.ModelForm):

    nombre = forms.CharField(required=True)
    valor = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(EntidadForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():

            field.widget.attrs.update({
                'class': 'form-control has-feedback-right'
            })

    class Meta:
        model = Entidad
        fields = '__all__'