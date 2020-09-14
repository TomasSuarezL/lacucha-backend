from app.ejercicios.model import Ejercicio
from flask import jsonify, request, abort
from flask_restx import Namespace, Resource

from app import db
from .service import EjercicioService

api = Namespace("Ejercicios", description="Ejercicios model")


@api.route('/')
class EjercicioResource(Resource):
    def get(self):
        from .model import Ejercicio
        _patron = request.args.get('patron', None)
        ejercicios = EjercicioService.get_por_nombre_patron(_patron)
        return jsonify([ex.to_json() for ex in ejercicios])

    def post(self):
        from .model import Ejercicio, PatronMovimiento
        _patron = request.args.get('patron', None)
        _nombre = request.args.get('nombre', None)
        ejercicio = EjercicioService.create_ejercicio(_nombre, _patron)

        db.session.add(ejercicio)
        db.session.commit()

        return jsonify(ejercicio.to_json())
