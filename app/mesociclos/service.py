from marshmallow.exceptions import ValidationError
from typing import List
from .model import Mesociclo, Objetivo, Organizacion
from app.sesiones.service import SesionService
from app.ejercicios.service import EjercicioService
from app.usuarios.service import UsuarioService
from app.usuarios.model import Nivel


class MesocicloService:
    @staticmethod
    def get_all_mesosiclos() -> List[Mesociclo]:
        return Mesociclo.query.all()

    @staticmethod
    def create_mesociclo(mesociclo: dict) -> Mesociclo:
        '''
        Crea un un objeto Mesociclo en base al dict deserealizado 

                Parameters:
                        mesociclo (dict): Estructura deserealizada enviada por el cliente
                        con informacion del mesociclo generado.

                Returns:
                        Mesociclo: objeto creado si los datos ingresados son validos.  
        '''

        usuario = UsuarioService.get_usuario_by_username(
            mesociclo["usuario"])
        if (usuario is None):
            raise ValidationError("Usuario Inválido")

        nivel = Nivel.query.filter_by(descripcion=mesociclo["nivel"]).first()
        if (nivel is None):
            raise ValidationError("Nivel Inválido")

        objetivo = Objetivo.query.filter_by(
            descripcion=mesociclo["objetivo"]).first()
        if (objetivo is None):
            raise ValidationError("Objetivo Inválido")

        organizacion = Organizacion.query.filter_by(
            descripcion=mesociclo["organizacion"]).first()
        if (organizacion is None):
            raise ValidationError("Organización Inválida")

        principal_tren_superior = EjercicioService.get_por_nombre(
            mesociclo["principal_tren_superior"])
        if (organizacion is None):
            raise ValidationError("Ejercicio Inválido - Tren Superior")

        principal_tren_inferior = EjercicioService.get_por_nombre(
            mesociclo["principal_tren_inferior"])
        if (organizacion is None):
            raise ValidationError("Ejercicio Inválido - Tren Inferior")

        sesiones = [SesionService.create_sesion(
            sesion) for sesion in mesociclo["sesiones"]]
        if (len(sesiones) == 0):
            raise ValidationError("Ingresar al menos 1 Sesión")

        newMesociclo = Mesociclo(
            usuario=usuario,
            nivel=nivel,
            objetivo=objetivo,
            organizacion=organizacion,
            principal_tren_superior=principal_tren_superior,
            principal_tren_inferior=principal_tren_inferior,
            semanas_por_mesociclo=mesociclo["semanas_por_mesociclo"],
            sesiones_por_semana=mesociclo["sesiones_por_semana"],
            sesiones=sesiones
        )

        return newMesociclo
