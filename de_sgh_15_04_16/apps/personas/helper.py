from .models import PersonaObraSocial


def existe_registro_persona_obra_social(persona, id_obrasocial):
    persona_obra_social = PersonaObraSocial.objects.filter(
        persona=persona).filter(obra_social=id_obrasocial)

    return True if persona_obra_social else False