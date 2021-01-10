from flask import request
from flask_restx import Namespace, Resource
from flask_accepts.decorators.decorators import accepts, responds

from app import db
from app.ejercicios.schema import EjercicioPostSchema, EjercicioSchema
from app.ejercicios.service import EjercicioService

api = Namespace("Ejercicios", description="Ejercicios model")


@api.route('/')
class EjercicioResource(Resource):
    @accepts(dict(name='patrones', type=str), api=api)
    @responds(schema=EjercicioSchema(many=True))
    def get(self):
        _patrones = request.parsed_args['patrones']
        if (_patrones != None):
            _patrones = _patrones.split(',')
        ejercicios = EjercicioService.get_por_nombre_patrones(_patrones)
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


string_list = "Traccion,Empuje"

string_list.split(',')
