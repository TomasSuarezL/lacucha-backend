from app.mesociclos.model import Mesociclo
from datetime import date
from typing import List
from app import db
from app.sesiones.model import Sesion
from .model import Usuario


class UsuarioService:
    @staticmethod
    def get_usuario_by_username(username: str) -> List[Usuario]:
        return Usuario.query.filter_by(username=username).first()

    @staticmethod
    def get_proxima_sesion(id_usuario: int) -> Sesion:
        '''
        Get the next Sesion of the current Mesociclo for the Usuario, if any. If there isn't any Sesion left to do in the Mesociclo, return None,
        thus we should suggets creating the next Mesociclo.   

                Parameters:
                        id_usuario (int): ID of the Usuario that we want to get the next Sesion.   

                Returns:
                        Sesion: Sesion object with the next Sesion to do. 
        '''

        mesociclo = Mesociclo.query.filter_by(
            id_usuario=id_usuario, id_estado=1).first()

        sesion = Sesion.query.filter_by(mesociclo=mesociclo, fecha_finalizado=None).order_by(
            Sesion.fecha_empezado.asc()).first()

        return sesion
