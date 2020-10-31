from app import db
from flask import jsonify, request, abort
from flask_accepts.decorators.decorators import accepts, responds
from flask_restx import Namespace, Resource
from marshmallow.utils import EXCLUDE

from .service import SesionService
from .schema import SesionSchema
# from datetime import date

api = Namespace("Sesiones", description="Sesiones model")


@api.route('/')
class SesionResource(Resource):
    def get(self):
        from .model import Sesion
        sesions = Sesion.query.order_by(Sesion.creado_en.desc()).all()
        return jsonify([ses.to_json() for ses in sesions])

    @accepts(schema=SesionSchema(session=db.session), api=api)
    @responds(schema=SesionSchema)
    def post(self):
        try:
            sesion = request.parsed_obj
            if not sesion:
                return {"message": "No se recibió información del bloque"}, 400

            newSesion = SesionService.create_sesion(sesion)

            db.session.add(newSesion)
            db.session.commit()

            return newSesion

        except AttributeError as err:
            print(err)
            abort(400, err)
        except:
            abort(400)


@api.route('/todaySession')
class TodaySesionResource(Resource):
    @responds(schema=SesionSchema)
    def get(self):
        sesion = SesionService.get_today_sesion()
        return sesion
