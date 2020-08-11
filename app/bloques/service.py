from marshmallow.utils import EXCLUDE
from marshmallow.exceptions import ValidationError
from app.ejercicios.model import Ejercicio
from app.ejercicios.service import EjercicioService
from typing import List
from .model import Bloque, EjercicioXBloque
from .schema import BloqueSchema, EjercicioXBloqueSchema


class BloqueService:
    @staticmethod
    def get_all_bloques() -> List[Bloque]:
        return Bloque.query.all()

    @staticmethod
    def create_ejercicio_x_bloque(ejercicio_bloque: dict) -> EjercicioXBloque:
        '''
        Crea un un objeto Ejercicio X Bloque en base al dict deserealizado 

                Parameters:
                        ejercicio_bloque (dict): Estructura deserealizada enviada por el cliente
                        con informacion del ejercicio realizado en el bloque.

                Returns:
                        EjercicioXBloque: objeto creado si el ejercicio ingresado es valido.  
        '''
        ejercicio = EjercicioService.get_por_nombre(
            ejercicio_bloque["ejercicio"]["nombre"])
        if (ejercicio is None):
            raise ValidationError("Ejercicio Inválido")

        ejercicio_x_bloque = EjercicioXBloque(
            ejercicio=ejercicio, repeticiones=ejercicio_bloque["repeticiones"], carga=ejercicio_bloque["carga"])

        return ejercicio_x_bloque

    @staticmethod
    def create_bloque(bloque: dict) -> Bloque:
        '''
        Crea un un objeto Bloque en base al dict deserealizado 

                Parameters:
                        bloque (dict): Estructura deserealizada enviada por el cliente
                        con informacion del bloque realizado en la sesion.

                Returns:
                        Bloque: objeto creado.  
        '''

        ejercicios = [BloqueService.create_ejercicio_x_bloque(
            ejercicio) for ejercicio in bloque["ejercicios"]]

        bloque = Bloque(
            ejercicios=ejercicios, series=bloque["series"], num_bloque=bloque["numBloque"])

        return bloque
