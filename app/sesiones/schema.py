from ast import dump
from marshmallow.fields import List, Nested
from marshmallow.utils import EXCLUDE
from marshmallow_sqlalchemy.schema.sqlalchemy_schema import SQLAlchemySchema, auto_field
from app import db
from app.bloques.schema import BloqueSchema, BloqueUpdateSchema
from app.sesiones.model import Sesion


class SesionSchema(SQLAlchemySchema):
    class Meta:
        model = Sesion
        load_instance = True
        unknown = EXCLUDE

    idSesion = auto_field("id_sesion", dump_only=True)
    bloques = List(Nested(BloqueSchema(session=db.session)))
    fechaEmpezado = auto_field("fecha_empezado", required=True)
    fechaFinalizado = auto_field("fecha_finalizado", dump_only=True)
    creadoEn = auto_field("creado_en", dump_only=True)
    actualizadoEn = auto_field("actualizado_en", dump_only=True)


class SesionUpdateSchema(SQLAlchemySchema):
    class Meta:
        model = Sesion
        load_instance = True

    idSesion = auto_field("id_sesion")
    bloques = List(Nested(BloqueUpdateSchema(session=db.session)))
    fechaEmpezado = auto_field("fecha_empezado")
    fechaFinalizado = auto_field("fecha_finalizado")
    creadoEn = auto_field("creado_en")
    actualizadoEn = auto_field("actualizado_en")
