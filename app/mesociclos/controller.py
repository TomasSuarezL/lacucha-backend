from marshmallow.exceptions import ValidationError
from app.mesociclos.service import MesocicloService
from app import db
from flask import jsonify, request, abort
from flask_accepts.decorators.decorators import accepts, responds
from flask_restx import Namespace, Resource
from marshmallow.utils import EXCLUDE
from .schema import MesocicloSchema

api = Namespace("Mesociclos", description="Mesociclo model")


@api.route('/')
class MesocicloResource(Resource):
    def get(self):
        from .model import Mesociclo
        mesociclos = Mesociclo.query.order_by(Mesociclo.creado_en.desc()).all()
        return jsonify([mes.to_json() for mes in mesociclos])

    @accepts(schema=MesocicloSchema, api=api)
    @responds(schema=MesocicloSchema)
    def post(self):
        mesociclo_schema = MesocicloSchema(unknown=EXCLUDE)

        try:
            body_mesociclo = request.get_json(force=True)
            if not body_mesociclo:
                return {"message": "No se recibió información del bloque"}, 400

            mesociclo = mesociclo_schema.load(body_mesociclo)
            newMesociclo = MesocicloService.create_mesociclo(mesociclo)

            db.session.add(newMesociclo)
            db.session.commit()

        except AttributeError as err:
            print(err)
            return err, 400
        except ValidationError as verr:
            return verr, 400
