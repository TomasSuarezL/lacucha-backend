
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


@api.route('/<int:id_usuario>/mesociclos/proximaSesion')
class NextSesionResource(Resource):
    @responds(schema=SesionSchema)
    def get(self, id_usuario):
        sesion = UsuarioService.get_proxima_sesion(id_usuario)
        return sesion
