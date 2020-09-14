from datetime import date
from app.bloques.service import BloqueService
from app import db
from typing import List
from .model import Usuario


class UsuarioService:
    @staticmethod
    def get_usuario_by_username(username: str) -> List[Usuario]:
        return Usuario.query.filter_by(username=username).first()
