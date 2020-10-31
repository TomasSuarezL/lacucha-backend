
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
