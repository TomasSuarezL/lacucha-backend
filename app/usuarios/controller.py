
from flask import request
from app.mesociclos.service import MesocicloService
from app.mesociclos.schema import MesocicloSchema
from app.sesiones.schema import SesionSchema
from app.usuarios.service import UsuarioService
from app.usuarios.schema import UsuarioSchema
from flask_accepts.decorators.decorators import accepts, responds
from flask_restx import Namespace, Resource

api = Namespace("Usuarios", description="Usuarios model")


@api.route('/<string:username>')
class UsuarioResource(Resource):
    @responds(schema=UsuarioSchema)
    def get(self, username):
        usuario = UsuarioService.get_usuario_by_username(username)

        return usuario


@api.route('/<int:id_usuario>/mesociclos')
class NextSesionResource(Resource):
    @accepts(dict(name='activo', type=bool), api=api)
    @responds(schema=MesocicloSchema(many=True))
    def get(self, id_usuario):
        _activo = request.parsed_args['activo']
        if _activo:
            return [MesocicloService.get_mesosiclo_activo_usuario(id_usuario)]
        else:
            return MesocicloService.get_all_mesosiclos_usuario(id_usuario)


@api.route('/<int:id_usuario>/mesociclos/proximaSesion')
class NextSesionResource(Resource):
    @responds(schema=SesionSchema)
    def get(self, id_usuario):
        sesion = UsuarioService.get_proxima_sesion(id_usuario)
        return sesion


@api.route('/<int:id_usuario>/mesociclos/sesionHoy')
class TodaySesionResource(Resource):
    @responds(schema=SesionSchema)
    def get(self, id_usuario):
        sesion = UsuarioService.get_today_sesion(id_usuario)
        return sesion
