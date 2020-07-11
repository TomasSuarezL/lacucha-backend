from flask import jsonify, request, abort
from flask_restx import Namespace, Resource

api = Namespace("Bloques", description="Bloques model")


@api.route('/')
class BloqueResource(Resource):
    def get(self):
        return jsonify("Not implemented yet")
