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

    @accepts(schema=SesionSchema, api=api)
    @responds(schema=SesionSchema)
    def post(self):
        sesion_schema = SesionSchema(unknown=EXCLUDE)

        try:
            body_sesion = request.get_json(force=True)
            if not body_sesion:
                return {"message": "No se recibió información del bloque"}, 400

            sesion = sesion_schema.load(body_sesion)
            newSesion = SesionService.create_sesion(sesion)

            db.session.add(newSesion)
            db.session.commit()

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
