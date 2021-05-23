from app.usuarios.service import UsuarioService
from marshmallow.utils import EXCLUDE
from marshmallow.exceptions import ValidationError
from flask import jsonify, request, abort
from flask_restx import Namespace, Resource
from flask_accepts import accepts, responds
from app import db, firebase
from app.bloques.schema import BloqueSchema, BloqueUpdateSchema
from app.bloques.service import BloqueService

api = Namespace("Bloques", description="Bloques model")


@api.route("/")
class BloqueResource(Resource):
    @firebase.jwt_required
    def get(self):
        return jsonify("Not implemented yet")

    @firebase.jwt_required
    @accepts(schema=BloqueSchema(session=db.session), api=api)
    @responds(schema=BloqueSchema)
    def post(self):
        try:
            # We can access to the object loaded by flask_accepts with request.parsed_obj
            bloque = request.parsed_obj

            newBloque = BloqueService.create_bloque(bloque)

            db.session.add(newBloque)
            db.session.commit()

            return newBloque
        except ValidationError as err:
            return err.messages, 422

    @firebase.jwt_required
    @accepts(schema=BloqueUpdateSchema(session=db.session), api=api)
    @responds(schema=BloqueSchema)
    def put(self):

        _uuid = request.jwt_payload["sub"]
        _usuario = UsuarioService.get_usuario_by_uuid(_uuid)
        try:
            bloque = request.parsed_obj

            if (
                bloque.sesiones.mesociclo.usuario.uuid != _uuid
                and _usuario.rol != "admin"
            ):
                return abort(400, "No tiene permisos para modificar el bloque")

            db.session.add(bloque)
            db.session.commit()

            return bloque
        except AttributeError as err:
            print(err)
            return err, 400
        except ValidationError as verr:
            print(verr)
            return verr, 400
