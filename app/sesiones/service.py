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
    def get_sesion_id(id: int) -> Sesion:
        return Sesion.query.get(id)

    @staticmethod
    def create_sesion(sesion: Sesion) -> Sesion:
        """
        Create an Sesion object from the Sesion resulting of the deserealization done by marshmallow-sqlalchemy that has
        just the attributes needed to create a new session.

                Parameters:
                        sesion (Sesion): Sesion deserealized as sent in the request body. We need to retrieve the objects referenced
                        in this object. In this case, the request's body contains just the Ejercicio name and we need to retrieve the
                        actual object from the DB with the given name, and the resulting Sesion should reference the existing Ejercicios  

                Returns:
                        Sesion: Sesion object created 
        """

        bloques = [BloqueService.create_bloque(bloque) for bloque in sesion.bloques]

        newSesion = Sesion(
            num_sesion=sesion.num_sesion,
            bloques=bloques,
            fecha_empezado=sesion.fecha_empezado,
        )

        return newSesion
