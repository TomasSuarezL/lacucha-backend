from app.mesociclos.service import MesocicloService
from datetime import date, datetime, timedelta
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
        thus we should suggest creating the next Mesociclo.   

                Parameters:
                        id_usuario (int): ID of the Usuario that we want to get the next Sesion.   

                Returns:
                        Sesion: Sesion object with the next Sesion to do. 
        '''

        mesociclo = MesocicloService.get_mesosiclo_activo_usuario(id_usuario)

        sesion = Sesion.query.filter_by(mesociclo=mesociclo, fecha_finalizado=None).order_by(
            Sesion.fecha_empezado.asc()).first()

        return sesion

    @staticmethod
    def get_today_sesion(id_usuario: int) -> Sesion:
        '''
        Get today's Sesion if any.   

                Parameters:
                        id_usuario (int): ID of the Usuario that we want to get the Sesion.   

                Returns:
                        Sesion or None: Sesion object with Session. 
        '''
        mesociclos = MesocicloService.get_all_mesosiclos_usuario(id_usuario)

        return Sesion.query.filter(
            Sesion.id_mesociclo.in_([m.id_mesociclo for m in mesociclos]),
            db.func.date(Sesion.fecha_empezado) == datetime.utcnow().date()
        ).first()
