from app import db
from typing import List
from .model import Sesion


class SesionService:
    @staticmethod
    def get_all_sesiones() -> List[Sesion]:
        return Sesion.query.all()
