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
    def get_por_nombre_patrones(patrones: List[str]) -> List[Ejercicio]:
        if (patrones is None):
            return Ejercicio.query.all()

        _patrones = PatronMovimiento.query.filter(
            PatronMovimiento.nombre.in_(patrones)).all()

        if (_patrones is None):
            return _patrones

        return Ejercicio.query.filter(Ejercicio.id_patron.in_([p.id_patron_movimiento for p in _patrones])).all()

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
