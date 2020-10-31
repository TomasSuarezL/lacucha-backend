from app.mesociclos.model import Mesociclo
from datetime import datetime
from flask import jsonify, request, abort
from flask_accepts.decorators.decorators import accepts, responds
from flask_restx import Namespace, Resource
from marshmallow.exceptions import ValidationError
from app import db
from app.mesociclos.service import MesocicloService
from .schema import MesocicloFlatSchema, MesocicloSchema

api = Namespace("Mesociclos", description="Mesociclo model")


@api.route('/')
class MesociclosResource(Resource):
    def get(self):
        from .model import Mesociclo
        mesociclos = Mesociclo.query.order_by(Mesociclo.creado_en.desc()).all()
        return jsonify([mes.to_json() for mes in mesociclos])

    @accepts(schema=MesocicloSchema(session=db.session), api=api)
    @responds(schema=MesocicloSchema)
    def post(self):
        try:
            mesociclo = request.parsed_obj

            if not mesociclo:
                return {"message": "No se recibió información del bloque"}, 400

            newMesociclo = MesocicloService.create_mesociclo(mesociclo)

            db.session.add(newMesociclo)
            db.session.commit()

            return newMesociclo

        except AttributeError as err:
            print(err)
            return err, 400
        except ValidationError as verr:
            return verr, 400

    @accepts(schema=MesocicloSchema(session=db.session), api=api)
    @responds(schema=MesocicloSchema)
    def put(self):
        try:
            mesociclo = request.parsed_obj

            if not mesociclo:
                return {"message": "No se recibió información del bloque"}, 400

            updatedMesiciclo = MesocicloService.create_mesociclo(mesociclo)
            updatedMesiciclo.actualizado_en = datetime.now()

            db.session.add(updatedMesiciclo)
            db.session.commit()

            return mesociclo

        except AttributeError as err:
            print(err)
            return err, 400
        except ValidationError as verr:
            return verr, 400


@api.route('/<int:id>')
class MesocicloResource(Resource):
    @responds(schema=MesocicloFlatSchema)
    def get(self, id):
        try:
            mesociclo = db.session.query(Mesociclo).get(id)
            return mesociclo
        except AttributeError as err:
            print(err)
            return err, 400
