from marshmallow.exceptions import ValidationError
from app.ejercicios.service import EjercicioService
from typing import List
from .model import Bloque, EjercicioXBloque


class BloqueService:
    @staticmethod
    def get_all_bloques() -> List[Bloque]:
        return Bloque.query.all()

    @staticmethod
    def create_ejercicio_x_bloque(ejercicio_bloque: EjercicioXBloque) -> EjercicioXBloque:
        '''
        Crea un un objeto Ejercicio X Bloque en base al dict deserealizado 

                Parameters:
                        ejercicio_bloque (EjercicoXBloque): Objeto EjercicioXBloque con los datos necesarios para
                        crear el ejercicoxbloque. En este caso recupera a partir del nombre del ejercicio, el objeto
                        Ejercicio referenciado ya existente.

                Returns:
                        EjercicioXBloque: objeto creado si el ejercicio ingresado es valido.  
        '''
        ejercicio = EjercicioService.get_por_nombre(
            ejercicio_bloque.ejercicio.nombre)
        if (ejercicio is None):
            raise ValidationError("Ejercicio Inválido")

        ejercicio_x_bloque = EjercicioXBloque(
            ejercicio=ejercicio, repeticiones=ejercicio_bloque.repeticiones, carga=ejercicio_bloque.carga)

        return ejercicio_x_bloque

    @staticmethod
    def create_bloque(bloque: Bloque) -> Bloque:
        '''
        Crea un un objeto Bloque en base al Bloque deserealizado por marshmallow-sqlalchemy 

                Parameters:
                        bloque (Bloque): Bloque solo con los datos necesarios para construir el bloque completo.
                        Es decir, primero hay que recuperar de la DB los objetos que fueran referenciados,
                        en este caso el ejercicio, que a partir del nombre obtengo el objeto ya exsitente que es
                        referenciado en el Bloque.

                Returns:
                        Bloque: objeto creado.  
        '''

        ejercicios = [BloqueService.create_ejercicio_x_bloque(
            ejercicio) for ejercicio in bloque.ejercicios]

        bloque = Bloque(
            ejercicios=ejercicios, series=bloque.series, num_bloque=bloque.num_bloque)

        return bloque
