'''
from apps.paciente.models import Paciente


def obtener_cuil_paciente(persona):
    consulta = Paciente.obejcts.filter(persona=persona)
    return consulta
'''
