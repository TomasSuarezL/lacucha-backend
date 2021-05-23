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
        unknown = EXCLUDE

    idEjerciciosxbloque = auto_field("id_ejerciciosxbloque", dump_only=True)
    ejercicio = Nested(EjercicioSchema(session=db.session, unknown=EXCLUDE))
    numEjercicio = auto_field("num_ejercicio", required=True)
    repeticiones = auto_field(required=True)
    carga = auto_field(required=True)


class EjercicioXBloqueUpdateSchema(SQLAlchemySchema):
    class Meta:
        model = EjercicioXBloque
        load_instance = True

    idEjerciciosxbloque = auto_field("id_ejerciciosxbloque", required=False)
    ejercicio = Nested(EjercicioSchema(session=db.session, unknown=EXCLUDE))
    numEjercicio = auto_field("num_ejercicio")
    repeticiones = auto_field()
    carga = auto_field()


class BloqueSchema(SQLAlchemySchema):
    class Meta:
        model = Bloque
        load_instance = True
        unknown = EXCLUDE

    idBloque = auto_field("id_bloque", dump_only=True)
    series = auto_field(required=True)
    numBloque = auto_field("num_bloque", required=True)
    ejercicios = List(Nested(EjercicioXBloqueSchema(session=db.session)))
    creadoEn = auto_field("creado_en", dump_only=True)
    actualizadoEn = auto_field("actualizado_en", dump_only=True)


class BloqueUpdateSchema(SQLAlchemySchema):
    class Meta:
        model = Bloque
        load_instance = True

    idBloque = auto_field("id_bloque")
    idSesion = auto_field("id_sesion", required=False)
    series = auto_field()
    numBloque = auto_field("num_bloque")
    ejercicios = List(Nested(EjercicioXBloqueUpdateSchema(session=db.session)))
    creadoEn = auto_field("creado_en")
    actualizadoEn = auto_field("actualizado_en")
