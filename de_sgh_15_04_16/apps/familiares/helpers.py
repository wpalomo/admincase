
def deshabilitar_campos(*forms):
    for form in forms:
        for name, field in form.fields.items():
            if name != 'numero_documento':
                field.widget.attrs.update({'disabled': 'disabled'})


def guardar_variable_session_familiar(id_familiar, request):

    request.session['id_familiar'] = id_familiar
    request.session['modulo_titulo'] = 'familiares'
