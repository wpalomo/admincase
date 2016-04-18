from django import forms

from .models import Institucion


class InstitucionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(InstitucionForm, self).__init__(*args, **kwargs)
        for name, field in list(self.fields.items()):
            field.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Institucion
        fields = '__all__'