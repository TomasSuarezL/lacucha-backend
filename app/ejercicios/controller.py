from flask import request
from flask_restx import Namespace, Resource
from flask_accepts.decorators.decorators import accepts, responds

from app import db
from app.ejercicios.schema import EjercicioPostSchema, EjercicioSchema
from app.ejercicios.service import EjercicioService

api = Namespace("Ejercicios", description="Ejercicios model")


@api.route('/')
class EjercicioResource(Resource):
    @accepts(dict(name='patron', type=str), api=api)
    @responds(schema=EjercicioSchema(many=True))
    def get(self):
        _patron = request.parsed_args['patron']
        ejercicios = EjercicioService.get_por_nombre_patron(_patron)
        return ejercicios

    @accepts(schema=EjercicioPostSchema(session=db.session), api=api)
    @responds(schema=EjercicioPostSchema)
    def post(self):
        body = request.get_json(force=True)
        _patron = body.get('patron', None)
        _nombre = body.get('nombre', None)
        ejercicio = EjercicioService.create_ejercicio(_nombre, _patron)

        db.session.add(ejercicio)
        db.session.commit()

        return ejercicio
