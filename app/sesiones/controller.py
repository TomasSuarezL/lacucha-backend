from app.bloques.service import BloqueService
from datetime import datetime
from flask import jsonify, request, abort
from flask_accepts.decorators.decorators import accepts, responds
from flask_restx import Namespace, Resource
from app import db, firebase

from .service import SesionService
from .schema import SesionSchema, SesionUpdateSchema

api = Namespace("Sesiones", description="Sesiones model")


@api.route("")
class SesionsResource(Resource):
    @firebase.jwt_required
    def get(self):
        from .model import Sesion

        sesions = Sesion.query.order_by(Sesion.creado_en.desc()).all()
        return jsonify([ses.to_json() for ses in sesions])

    @firebase.jwt_required
    @accepts(schema=SesionSchema(session=db.session), api=api)
    @responds(schema=SesionSchema)
    def post(self):
        try:
            sesion = request.parsed_obj
            if not sesion:
                return {"message": "No se recibió información de la sesión."}, 400

            db.session.add(sesion)
            db.session.commit()

            return sesion

        except AttributeError as err:
            print(err)
            abort(400, err)
        except Exception as e:
            abort(400, str(e))


@api.route("/<int:id_sesion>")
class SesionResource(Resource):
    @firebase.jwt_required
    @accepts(schema=SesionUpdateSchema(session=db.session), api=api)
    @responds(schema=SesionSchema)
    def put(self, id_sesion):
        try:
            sesion = request.parsed_obj
            sesion.actualizado_en = datetime.utcnow()

            db.session.add(sesion)
            db.session.commit()

            return sesion

        except AttributeError as err:
            print(err)
            abort(400, err)
