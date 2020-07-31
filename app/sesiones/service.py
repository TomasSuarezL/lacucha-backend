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
    def create_sesion(sesion: dict) -> Sesion:

        bloques = [BloqueService.create_bloque(
            bloque) for bloque in sesion["bloques"]]

        newSesion = Sesion(
            bloques=bloques, fecha_empezado=sesion["empezado"], fecha_finalizado=sesion["finalizado"])

        return newSesion
