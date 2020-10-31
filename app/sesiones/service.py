from datetime import date
from marshmallow.exceptions import ValidationError
from marshmallow.utils import EXCLUDE
from app.sesiones.schema import SesionSchema
from app.bloques.service import BloqueService
from app import db
from typing import List
from .model import Sesion


class SesionService:
    @staticmethod
    def get_all_sesiones() -> List[Sesion]:
        return Sesion.query.all()

    @staticmethod
    def get_today_sesion() -> Sesion:
        return Sesion.query.filter(Sesion.creado_en >= date.today()).order_by(Sesion.creado_en.desc()).first()

    @staticmethod
    def create_sesion(sesion: Sesion) -> Sesion:
        '''
        Create an Sesion object from the Sesion resulting of the deserealization done by marshmallow-sqlalchemy that has
        just the attributes needed to create a new session.

                Parameters:
                        sesion (Sesion): Sesion deserealized as sent in the request body. We need to retrieve the objects referenced
                        in this object. In this case, the request's body contains just the Ejercicio name and we need to retrieve the
                        actual object from the DB with the given name, and the resulting Sesion should reference the existing Ejercicios  

                Returns:
                        Sesion: Sesion object created 
        '''

        bloques = [BloqueService.create_bloque(
            bloque) for bloque in sesion.bloques]

        newSesion = Sesion(
            bloques=bloques, fecha_empezado=sesion.fecha_empezado, fecha_finalizado=sesion.fecha_finalizado)

        return newSesion
