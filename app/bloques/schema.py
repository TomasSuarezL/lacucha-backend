from marshmallow.fields import List, Nested
from marshmallow.utils import EXCLUDE
from marshmallow_sqlalchemy.schema.sqlalchemy_schema import SQLAlchemySchema, auto_field
from app import db
from app.bloques.model import Bloque, EjercicioXBloque
from app.ejercicios.schema import EjercicioSchema


class EjercicioXBloqueSchema(SQLAlchemySchema):
    class Meta:
        model = EjercicioXBloque
        load_instance = True

    id_ejerciciosxbloque = auto_field(dump_only=True)
    ejercicio = Nested(EjercicioSchema(session=db.session, unknown=EXCLUDE))
    repeticiones = auto_field(required=True)
    carga = auto_field(required=True)


class BloqueSchema(SQLAlchemySchema):
    class Meta:
        model = Bloque
        load_instance = True

    id_bloque = auto_field(dump_only=True)
    series = auto_field(required=True)
    numBloque = auto_field("num_bloque", required=True)
    ejercicios = List(Nested(EjercicioXBloqueSchema(session=db.session)))
    creado_en = auto_field(dump_only=True)
    actualizado_en = auto_field(dump_only=True)
