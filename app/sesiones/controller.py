from flask import jsonify, request, abort
from flask_restx import Namespace, Resource
from cerberus import Validator

from .service import SesionService
from datetime import date

api = Namespace("Sesiones", description="Sesiones model")

# NEW POST SCHEMA VALIDATION FOR REQUEST BODY.
ejercicioSchema = {
    'type': 'dict',
    'schema': {
        "nombre": {'type': 'string', 'required': True},
        "zona": {'type': 'string', 'required': False},
        "carga": {'type': 'float', 'required': False},
        "repeticiones": {'type': 'integer', 'required': True}
    }
}

bloqueSchema = {
    'type': 'dict',
    'schema': {
        'numBloque': {'type': 'integer', 'required': True},
        'series': {'type': 'integer', 'required': True},
        "ejercicios": {'type': 'list', 'schema': ejercicioSchema}
    }
}

sesionSchema = {
    'empezado': {'type': 'string', 'required': True},
    'finalizado': {'type': 'string', 'required': True},
    'bloques': {'type': 'list', 'schema': bloqueSchema},
}

sesionValidator = Validator(sesionSchema)


@api.route('/')
class SesionResource(Resource):
    def get(self):
        from .model import Sesion
        sesions = Sesion.query.order_by(Sesion.creado_en.desc()).all()
        return jsonify([ses.to_json() for ses in sesions])

    def post(self):
        from app.bloques import Bloque
        from app.bloques import EjercicioXBloque
        from app.ejercicios import Ejercicio
        from app.sesiones import Sesion
        from app import db
        bodySesion = request.get_json(force=True)

        try:
            # Validate body of request
            if(not sesionValidator.validate(bodySesion, sesionSchema)):
                abort(
                    400, f"Invalid Body. Errors: {str(sesionValidator.errors)} \n post schema: {str(sesionSchema)}")

            bloques = [Bloque(ejercicios=[EjercicioXBloque(
                ejercicio=EjercicioXBloque.query.filter_by(
                    nombre=exercise.get("nombre")).first(),
                carga=exercise.get("carga"),
                repeticiones=exercise.get("repeticiones"))
                for exercise in block.get('ejercicios')],
                block_num=block.get('numBloque'), series=block.get('series'))
                for block in bodySesion.get('bloques')]

            sesion = Sesion(bloques=bloques, fecha_empezado=bodySesion.get(
                'empezado'), fecha_finalizado=bodySesion.get('finalizado'))

            db.session.add(sesion)
            db.session.commit()

            return "Session Created", 200
        except AttributeError as err:
            print(err)
            return err, 400
        except:
            return 400


@api.route('/todaySession')
class TodaySesionResource(Resource):
    def get(self):
        from .model import Sesion
        sesion = Sesion.query.filter(Sesion.creado_en >= date.today(
        )).order_by(Sesion.creado_en.desc()).first()
        return jsonify(sesion.to_json() if sesion != None else sesion)
