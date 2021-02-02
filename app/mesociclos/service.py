from app.sesiones.model import Sesion
from marshmallow.exceptions import ValidationError
from typing import List
from .model import Mesociclo
from app.sesiones.service import SesionService


class MesocicloService:
    @staticmethod
    def get_all_mesosiclos() -> List[Mesociclo]:
        return Mesociclo.query.all()

    @staticmethod
    def get_all_mesosiclos_usuario(id_usuario: int) -> List[Mesociclo]:
        '''
        List ALL Mesociclos of the specified Usuario, by its id (id_usuario). 

                Parameters:
                        id_usuario (int): ID of the Usuario which we want to get the Mesociclos.

                Returns:
                        List[Mesociclo]: List of Mesociclos for the Usuario.  
        '''
        return Mesociclo.query.filter_by(id_usuario=id_usuario).all()

    @staticmethod
    def get_mesosiclo_activo_usuario(id_usuario: int) -> Mesociclo:
        '''
        Get the active (estado activo) Mesociclo of the specified Usuario, by its id (id_usuario). 

                Parameters:
                        id_usuario (int): ID of the Usuario which we want to get the active Mesociclo.

                Returns:
                        Mesociclo: Active Mesociclo for the Usuario.  
        '''
        return Mesociclo.query.filter_by(id_usuario=id_usuario, id_estado=1).first()

    @staticmethod
    def create_mesociclo(mesociclo: Mesociclo) -> Mesociclo:
        '''
        Create a new Mesociclo object from the deserealized data recieved in the request

                Parameters:
                        mesociclo (Mesociclo): Object that was deserealized by marshmallow-sqlalchemy. The Sesions doesn't get referenced
                        by the package (the IDs are not provided, this could be updated), so we need to create them with the data that was
                        provided.

                Returns:
                        Mesociclo: new object created.  
        '''

        sesiones = [SesionService.create_sesion(
            sesion) for sesion in mesociclo.sesiones]
        if (len(sesiones) == 0):
            raise ValidationError("Ingresar al menos 1 Sesión")

        mesociclo.sesiones = sesiones

        return mesociclo
