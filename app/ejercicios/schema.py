
from marshmallow.fields import Pluck
from marshmallow.utils import EXCLUDE
from marshmallow_sqlalchemy.schema.sqlalchemy_schema import SQLAlchemySchema, auto_field
from app.ejercicios.model import Ejercicio, PatronMovimiento
from app import db


class PatronSchema(SQLAlchemySchema):
    class Meta:
        model = PatronMovimiento
        load_instance = True

    nombre = auto_field()
    creado_en = auto_field(dump_only=True)
    actualizado_en = auto_field(dump_only=True)


class EjercicioSchema(SQLAlchemySchema):
    class Meta:
        model = Ejercicio
        load_instance = True
        unknown = EXCLUDE

    idEjercicio = auto_field("id_ejercicio")
    nombre = auto_field()
    patron = Pluck(PatronSchema(session=db.session), 'nombre', dump_only=True)
    urlVideo = auto_field("url_video")
    creado_en = auto_field(dump_only=True)
    actualizado_en = auto_field(dump_only=True)


# SCHEMA usado para crear un ejercicio nuevo: lo diferencio porque necesito solo nombre y patron. Mientras que
# en un request de crear Mesociclo/Sesion/Bloque, solo necesito el nombre (Uso el schema completo pero requiere solo este campo)
class EjercicioPostSchema(SQLAlchemySchema):
    class Meta:
        model = Ejercicio
        load_instance = True
        unknown = EXCLUDE

    nombre = auto_field(required=True)
    patron = Pluck(PatronSchema(session=db.session), 'nombre', required=True)
    urlVideo = auto_field('url_video')
