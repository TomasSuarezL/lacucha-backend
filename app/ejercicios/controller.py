from flask import request, abort
from flask_restx import Namespace, Resource
from flask_accepts.decorators.decorators import accepts, responds

from app import db, firebase
from app.ejercicios.schema import (
    EjercicioPostSchema,
    EjercicioPutSchema,
    EjercicioSchema,
)
from app.ejercicios.service import EjercicioService
from app.usuarios.service import UsuarioService

api = Namespace("Ejercicios", description="Ejercicios model")


@api.route("")
class EjercicioResource(Resource):
    @firebase.jwt_required
    @accepts(dict(name="patrones", type=str), api=api)
    @responds(schema=EjercicioSchema(many=True))
    def get(self):
        _patrones = request.parsed_args["patrones"]
        if _patrones != None:
            _patrones = _patrones.split(",")
        ejercicios = EjercicioService.get_por_nombre_patrones(_patrones)
        return ejercicios

    @firebase.jwt_required
    @accepts(schema=EjercicioPostSchema(session=db.session), api=api)
    @responds(schema=EjercicioPostSchema)
    def post(self):
        body = request.get_json(force=True)
        _patron = body.get("patron", None)
        _nombre = body.get("nombre", None)
        ejercicio = EjercicioService.create_ejercicio(_nombre, _patron)

        db.session.add(ejercicio)
        db.session.commit()

        return ejercicio


@api.route("/<string:id>")
class EjercicioUpdateResource(Resource):
    @firebase.jwt_required
    @accepts(schema=EjercicioPutSchema(session=db.session), api=api)
    @responds(schema=EjercicioSchema)
    def put(self, id):
        try:
            usuario = UsuarioService.get_usuario_by_uuid(request.jwt_payload["sub"])

            if usuario.rol != "admin":
                return abort(403, "No tiene permisos para acceder a este usuario.")

            ejercicio = request.parsed_obj

            db.session.add(ejercicio)
            db.session.commit()
            return ejercicio

        except AttributeError as err:
            print(err)
            return abort(400, str(err))

        except Exception as e:
            print(str(e))
            return abort(400, e)

