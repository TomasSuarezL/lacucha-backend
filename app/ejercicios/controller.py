from flask import jsonify, request, abort
from flask_restx import Namespace, Resource

from .service import EjercicioService

api = Namespace("Ejercicios", description="Ejercicios model")


@api.route('/')
class EjercicioResource(Resource):
    def get(self):
        from .model import Ejercicio
        _patron = request.args.get('patron', None)
        ejercicios = EjercicioService.get_por_nombre_patron(_patron)
        return jsonify([ex.to_json() for ex in ejercicios])
