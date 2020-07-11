from app import db
from typing import List
from .model import Bloque, EjercicioXBloque


class BloqueService:
    @staticmethod
    def get_all_bloques() -> List[Bloque]:
        return Bloque.query.all()
