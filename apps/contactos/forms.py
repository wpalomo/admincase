
from django import forms
from django.forms.utils import ErrorList

from .models import Contacto, TipoContacto

proveedores = (
    ('', '------'),
    ('Telecom', 'Telecom'),
    ('Personal', 'Personal'),
    ('Movistar', 'Movistar'),
    ('Claro', 'Claro'),
    ('Otro', 'Otro'),
)


class ContactoForm(forms.ModelForm):

    proveedor = forms.ChoiceField(choices=proveedores, required=False)
    tipo_contacto = forms.ModelChoiceField(queryset=TipoContacto.objects.all(),
                                           required=True)
    descripcion = forms.CharField(required=True)
    observacion = forms.CharField(required=False, widget=forms.Textarea())

    def __init__(self, *args, **kwargs):
        super(ContactoForm, self).__init__(*args, **kwargs)

        for name, field in list(self.fields.items()):
            field.widget.attrs.update({'class': 'form-control'})

    def clean(self):
        # print(self.cleaned_data['tipo_contacto'])
        # if str(self.cleaned_data['tipo_contacto']) == 'INTERNO':
        #                 print('acaaaaa')
        #                 print(RegexValidator(r'[0-9]+', self.cleaned_data['descripcion']))
        #                 if not re.match(r'[0-9]+', self.cleaned_data['descripcion']):
        #                     errors = self._errors.setdefault("descripcion",
        #                                                      ErrorList())
        #                     errors.append('Ingrese un formato correcto')
        if not self.instance.pk:
            if 'descripcion' in self.cleaned_data:
                if 'tipo_contacto' in self.cleaned_data:
                    if Contacto.objects.filter(descripcion=self.cleaned_data['descripcion'],
                                               tipo_contacto=self.cleaned_data['tipo_contacto']).exists():
                        errors = self._errors.setdefault("descripcion",
                                                             ErrorList())
                        errors.append('Ya registro este contacto')
        return super(ContactoForm, self).clean()

    class Meta:
        model = Contacto
        fields = ['proveedor', 'tipo_contacto', 'descripcion', 'observacion']
