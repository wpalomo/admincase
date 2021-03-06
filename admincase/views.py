from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext

from datetime import date, datetime, timedelta

from apps.personas.models import Persona
from apps.tramites.models import Tramite


def autenticarse(request):
    if not request.user.is_authenticated():
        return render(request, 'login.html', {
            'mensaje': '', 'action': 'autenticar_usuario'})
    else:
        return inicio(request)


def reset_password(request):
        return render(request, 'reset_password.html')


def autenticar_usuario(request):
    user = authenticate(
        username=request.POST['usuario'],
        password=request.POST['password'])

    count_login_error = request.POST['contador_login']

    if user is not None:
        if user.is_active:
            # if request.POST['usuario'] == request.POST['password']:
            #     return render(request, 'login.html', {'mensaje': 'Debe cambiar su contraseña.',
            #         'usuario': request.POST['usuario'],
            #         'alert': 'warning',
            #         'action': 'modificar_password'
            #         })
            # else:
            login(request, user)
            return redirect('/inicio')
        else:
            return render(request, 'login.html', {
                'mensaje': 'Su cuenta se ecuentra deshabilitada.',
                'alert': 'danger', 'action': 'autenticar_usuario'})
    else:
        count_login_error = int(count_login_error) + 1
        error_login = (count_login_error, 3)[count_login_error >= 3]

        return render(request, 'login.html', {
            'mensaje': 'El nombre de usuario o contraseña son incorrectos.',
            'alert': 'danger', 'action': 'autenticar_usuario',
            'error_login': error_login
        })


def salir(request):
    logout(request)
    return redirect('/inicio')


def get_novedades():
    """
    lt es menor
    lte es menor e igual
    gt es mayor
    gte es mayor e igual
    """

    fecha = datetime.now()
    dias = timedelta(days=20)
    fecha_limite = fecha - dias
    print(fecha_limite)
    tramites_alarma = Tramite.objects.filter(
        fecha_turno__gte=fecha,
        fecha_alarma__gte=fecha_limite).order_by('fecha_turno')

    # 11/08/2016

    return tramites_alarma


@login_required(login_url='/')
def inicio(request):

    persona = Persona.objects.filter(numero_documento=request.user.username)

    request.session['institucion_local'] = 'HAC'

    if len(persona) > 0:
        request.session['foto'] = persona[0].foto
    else:
        request.session['foto'] = 'usuario.png'

    return render_to_response('home.html', {
        'usuario': request.user,
        'novedades': get_novedades()
    }, context_instance=RequestContext(request))


@login_required(login_url='/')
def ayuda(request):
    usuario = request.user
    fecha = date.today()
    return render_to_response('ayuda.html', {
        'usuario': usuario, 'fecha': fecha},
        context_instance=RequestContext(request))


@login_required(login_url='/')
def internos(request):
    usuario = request.user
    fecha = date.today()
    return render_to_response('internos.html',
                              {'usuario': usuario, 'fecha': fecha},
                              context_instance=RequestContext(request))
