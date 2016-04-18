'''
from .models import Paciente

def get_numero_autoincremental_paciente():
    return: Devuelve el ultimo id de paciente
    qs_maximo_id_paciente = Paciente.objects.latest('id')
    maximo_id_paciente = str(int(qs_maximo_id_paciente.id + 1))
    return '%s' % maximo_id_paciente
'''