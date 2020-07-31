from marshmallow.utils import EXCLUDE
from marshmallow.exceptions import ValidationError
from flask import jsonify, request, abort
from flask_restx import Namespace, Resource
from flask_accepts import accepts, responds
from app import db
from app.bloques.schema import BloqueSchema
from app.bloques.service import BloqueService

api = Namespace("Bloques", description="Bloques model")


@api.route('/')
class BloqueResource(Resource):
    def get(self):
        return jsonify("Not implemented yet")

    @accepts(schema=BloqueSchema, api=api)
    @responds(schema=BloqueSchema)
    def post(self):
        bloque_schema = BloqueSchema(unknown=EXCLUDE)

        try:
            bloque_data = request.get_json()
            if not bloque_data:
                return {"message": "No se recibió información del bloque"}, 400

            bloque = bloque_schema.load(bloque_data)

            newBloque = BloqueService.create_bloque(bloque)

            return newBloque
        except ValidationError as err:
            return err.messages, 422
