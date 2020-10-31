from app import db
from typing import List
from .model import Ejercicio, PatronMovimiento


class EjercicioService:
    @staticmethod
    def get_por_nombre(nombre: str) -> Ejercicio:
        '''
        Devuelve el Ejercicio a partir del nombre

                Parameters:
                        nombre (string): El nombre del ejercicio

                Returns:
                        Ejercicio or None: objeto de clase Ejercicio si fue encontrado en BD o None si no encuentra  
        '''
        return Ejercicio.query.filter_by(nombre=nombre).first()

    @staticmethod
    def get_por_nombre_patron(patron: str) -> List[Ejercicio]:
        if (patron is None):
            return Ejercicio.query.all()

        _patron = PatronMovimiento.query.filter(
            PatronMovimiento.nombre == patron).first()
        return Ejercicio.query.filter(Ejercicio.patron == _patron).all()

    @staticmethod
    def create_ejercicio(nombre: str, patron: str) -> Ejercicio:
        '''
        Crea un objeto de la clase Ejercicio con el nombre y patron indicados 

                Parameters:
                        nombre (string): El nombre del ejercicio
                        patron: Patron de movimiento del

                Returns:
                        Ejercicio: objeto creado.  
        '''
        if(nombre is None or nombre == ""):
            return "Nombre inválido."

        _patron = PatronMovimiento.query.filter_by(nombre=patron).first()

        if(_patron is None):
            return "Patron inválido."

        nuevoEjercicio = Ejercicio(
            nombre=nombre, patron=_patron)

        return nuevoEjercicio
