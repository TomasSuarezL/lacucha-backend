from marshmallow.utils import EXCLUDE
from marshmallow.exceptions import ValidationError
from flask import jsonify, request, abort
from flask_restx import Namespace, Resource
from flask_accepts import accepts, responds
from app import db, firebase
from app.bloques.schema import BloqueSchema
from app.bloques.service import BloqueService

api = Namespace("Bloques", description="Bloques model")


@api.route('/')
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
