from datetime import datetime
from sqlalchemy import exc
from flask import request, abort
from flask_restx import Namespace, Resource
from flask_accepts.decorators.decorators import accepts, responds
from app.mesociclos.service import MesocicloService
from app.mesociclos.schema import MesocicloSchema
from app.sesiones.schema import SesionSchema
from app.usuarios.service import UsuarioService
from app.usuarios.schema import UsuarioSchema
from app import db, firebase

api = Namespace("Usuarios", description="Usuarios model")


@api.route("/")
class CreateUsuarioResource(Resource):
    @firebase.jwt_required
    @accepts(schema=UsuarioSchema(session=db.session), api=api)
    @responds(schema=UsuarioSchema)
    def post(self):
        try:
            usuario = request.parsed_obj
            if not usuario:
                return {"message": "Usuario invalido."}

            db.session.add(usuario)
            db.session.commit()
        except exc.IntegrityError as e:
            return abort(400, "El usuario o el email ya existen.")
        except:
            return "Error al guardar el usuario", 500
        return usuario

    @firebase.jwt_required
    @responds(schema=UsuarioSchema(many=True))
    def get(self):
        try:
            _search = request.args["search"] or ""
            usuario = UsuarioService.get_usuario_by_uuid(request.jwt_payload["sub"])

            if usuario.rol != "admin":
                return abort(403, "No tiene permisos para acceder a este usuario.")

            usuarios = UsuarioService.get_usuarios(_search)

        except Exception as e:
            return abort(400, str(e))

        return usuarios


@api.route("/<string:uuid>")
class UsuarioResource(Resource):
    @firebase.jwt_required
    @responds(schema=UsuarioSchema)
    def get(self, uuid):
        usuario = UsuarioService.get_usuario_by_uuid(uuid)

        if usuario.uuid != request.jwt_payload["sub"]:
            return abort(403, "No tiene permisos para acceder a este usuario.")

        return usuario

    @firebase.jwt_required
    @accepts(schema=UsuarioSchema(session=db.session), api=api)
    @responds(schema=UsuarioSchema)
    def put(self, uuid):
        try:
            usuario = request.parsed_obj
            if not usuario:
                return {"message": "Usuario invalido."}

            usuario.actualizado_en = datetime.utcnow()

            db.session.add(usuario)
            db.session.commit()
        except exc.IntegrityError as e:
            return abort(400, "El usuario o el email ya existen.")
        except:
            return "Error al guardar el usuario", 500
        return usuario


@api.route("/<int:id_usuario>/mesociclos")
class MesocicloResource(Resource):
    @firebase.jwt_required
    @accepts(dict(name="activo", type=bool), api=api)
    @responds(schema=MesocicloSchema(many=True))
    def get(self, id_usuario):
        _activo = request.parsed_args["activo"]
        if _activo:
            return [MesocicloService.get_mesosiclo_activo_usuario(id_usuario)]
        else:
            return MesocicloService.get_all_mesosiclos_usuario(id_usuario)


@api.route("/<int:id_usuario>/mesociclos/proximaSesion")
class NextSesionResource(Resource):
    @firebase.jwt_required
    @responds(schema=SesionSchema)
    def get(self, id_usuario):
        sesion = UsuarioService.get_proxima_sesion(id_usuario)
        return sesion


@api.route("/<int:id_usuario>/mesociclos/sesionHoy")
class TodaySesionResource(Resource):
    @firebase.jwt_required
    @responds(schema=SesionSchema)
    def get(self, id_usuario):
        sesion = UsuarioService.get_today_sesion(id_usuario)
        return sesion
