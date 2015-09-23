from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext

from datetime import date

from apps.personas.models import Persona


def autenticarse(request):
    if not request.user.is_authenticated():
        return render(request, 'login.html', {'mensaje': '', 'action': 'autenticar_usuario'})
    else:
        return inicio(request)


def autenticar_usuario(request):
    acceso = authenticate(username=request.POST['usuario'], password=request.POST['password'])
    # print("asdfd")
    if acceso is not None:
        if acceso.is_active:
            # if request.POST['usuario'] == request.POST['password']:
            #     return render(request, 'login.html', {'mensaje': 'Debe cambiar su contraseña.',
            #         'usuario': request.POST['usuario'],
            #         'alert': 'warning',
            #         'action': 'modificar_password'
            #         })
            # else:
            login(request, acceso)
            return redirect('/inicio')
        else:
            return render(request, 'login.html',
            {'mensaje': 'Su cuenta se ecuentra deshabilitada.', 'alert': 'danger', 'action': 'autenticar_usuario'})
    else:
        return render(request, 'login.html', {'mensaje': 'El nombre de usuario o contraseña son incorrectos.',
            'alert': 'danger', 'action': 'autenticar_usuario'})


def salir(request):
    logout(request)
    return redirect('/inicio')


@login_required(login_url='/')
def inicio(request):
    usuario = request.user
    persona = Persona.objects.filter(numero_documento=usuario.username)

    request.session['institucion_local'] = 'HAC'

    if len(persona) > 0:
        request.session['foto'] = persona[0].foto
    else:
        request.session['foto'] = 'usuario.png'

    return render_to_response('home.html', {
        'usuario': usuario
    }, context_instance=RequestContext(request))


@login_required(login_url='/')
def ayuda(request):
    usuario = request.user
    fecha = date.today()
    return render_to_response('ayuda.html',
        {'usuario': usuario, 'fecha': fecha},
        context_instance=RequestContext(request))


@login_required(login_url='/')
def internos(request):
    usuario = request.user
    fecha = date.today()
    return render_to_response('internos.html',
        {'usuario': usuario, 'fecha': fecha},
        context_instance=RequestContext(request))
