from flask.globals import session
from app.mesociclos.model import Mesociclo
from datetime import datetime
from flask import jsonify, request, abort
from flask_accepts.decorators.decorators import accepts, responds
from flask_restx import Namespace, Resource
from marshmallow.exceptions import ValidationError
from app import db
from app.mesociclos.service import MesocicloService
from .schema import MesocicloUpdateSchema, MesocicloSchema

api = Namespace("Mesociclos", description="Mesociclo model")


@api.route('/')
class MesociclosResource(Resource):
    def get(self):
        from .model import Mesociclo
        mesociclos = Mesociclo.query.order_by(Mesociclo.creado_en.desc()).all()
        return jsonify([mes.to_json() for mes in mesociclos])

    # @accepts(schema=MesocicloSchema(session=db.session), api=api)
    @responds(schema=MesocicloSchema(session=db.session))
    def post(self):
        try:
            mesociclo = request.get_json()

            if not mesociclo:
                return {"message": "No se recibió información del mesociclo"}, 400

            mesosciclo_schema = MesocicloSchema(session=db.session)
            mesociclo = mesosciclo_schema.load(mesociclo)

            newMesociclo = MesocicloService.create_mesociclo(mesociclo)

            db.session.add(newMesociclo)
            db.session.commit()

            return newMesociclo

        except AttributeError as err:
            print(err)
            return err, 400
        except ValidationError as verr:
            return verr, 400


@api.route('/<int:id>')
class MesocicloResource(Resource):
    @responds(schema=MesocicloSchema)
    def get(self, id):
        try:
            mesociclo = db.session.query(Mesociclo).get(id)
            return mesociclo
        except AttributeError as err:
            print(err)
            return err, 400

    @accepts(schema=MesocicloUpdateSchema(session=db.session), api=api)
    @responds(schema=MesocicloSchema)
    def put(self, id):
        try:
            sentMesociclo = request.parsed_obj
            if not sentMesociclo:
                return {"message": "No se recibió información del mesociclo"}, 400

            sentMesociclo.actualizado_en = datetime.utcnow()

            db.session.add(sentMesociclo)
            db.session.commit()

            return sentMesociclo

        except AttributeError as err:
            print(err)
            return err, 400
        except ValidationError as verr:
            return verr, 400
