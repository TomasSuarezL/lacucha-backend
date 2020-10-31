from marshmallow.fields import List, Nested
from marshmallow_sqlalchemy.schema.sqlalchemy_schema import SQLAlchemySchema, auto_field
from app import db
from app.bloques.schema import BloqueSchema
from app.sesiones.model import Sesion


class SesionSchema(SQLAlchemySchema):
    class Meta:
        model = Sesion
        load_instance = True

    id_sesion = auto_field(dump_only=True)
    bloques = List(Nested(BloqueSchema(session=db.session)))
    fechaEmpezado = auto_field("fecha_empezado")
    fechaFinalizado = auto_field("fecha_finalizado")
    creado_en = auto_field(dump_only=True)
    actualizado_en = auto_field(dump_only=True)
