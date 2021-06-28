from app.plantillas.schema import PlantillaSchema
from app.plantillas.model import Plantilla
from app.usuarios.service import UsuarioService
from marshmallow.exceptions import ValidationError
from flask import request, abort
from flask_restx import Namespace, Resource
from flask_accepts import accepts, responds
from app import db, firebase

api = Namespace("Plantillas", description="Plantillas model")


@api.route("")
class PlantillaResource(Resource):
    @firebase.jwt_required
    @responds(schema=PlantillaSchema(many=True))
    def get(self):
        try:
            _uuid = request.jwt_payload["sub"]
            _usuario = UsuarioService.get_usuario_by_uuid(_uuid)
            if _usuario.rol != "admin":
                return abort(403, "No tiene permisos para ver plantillas")

            return Plantilla.query.all()
        except AttributeError as err:
            print(err)
            return err, 400
        except ValidationError as err:
            print(err)
            return err, 400
        except Exception as err:
            print(err)
            abort(400, err)

    @firebase.jwt_required
    @accepts(schema=PlantillaSchema(session=db.session), api=api)
    @responds(schema=PlantillaSchema)
    def post(self):
        try:
            # We can access to the object loaded by flask_accepts with request.parsed_obj
            plantilla = request.parsed_obj

            db.session.add(plantilla)
            db.session.commit()

            return plantilla
        except ValidationError as err:
            return err.messages, 422
        except Exception as err:
            return str(err), 400

    @firebase.jwt_required
    @accepts(schema=PlantillaSchema(session=db.session), api=api)
    @responds(schema=PlantillaSchema)
    def put(self):
        try:
            _uuid = request.jwt_payload["sub"]
            _usuario = UsuarioService.get_usuario_by_uuid(_uuid)
            plantilla = request.parsed_obj

            if _usuario.rol != "admin":
                return abort(403, "No tiene permisos para modificar la plantilla")

            db.session.add(plantilla)
            db.session.commit()

            return plantilla
        except AttributeError as err:
            print(err)
            return err, 400
        except ValidationError as verr:
            print(verr)
            return verr, 400


@api.route("/<int:id>")
class PlantillaDeleteResource(Resource):
    @firebase.jwt_required
    def delete(self, id):
        try:
            plantilla = Plantilla.query.filter(Plantilla.id_plantilla == id).first()
            db.session.delete(plantilla)
            db.session.commit()
            return True
        except ValidationError as err:
            return err.messages, 422
        except Exception as err:
            return str(err), 400
