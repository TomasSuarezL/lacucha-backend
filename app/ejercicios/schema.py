from marshmallow.fields import Nested, Pluck
from marshmallow.utils import EXCLUDE
from marshmallow_sqlalchemy.schema.sqlalchemy_schema import SQLAlchemySchema, auto_field
from app.ejercicios.model import Ejercicio, PatronMovimiento
from app import db


class PatronSchema(SQLAlchemySchema):
    class Meta:
        model = PatronMovimiento
        load_instance = True
        unknown = EXCLUDE

    idPatron = auto_field("id_patron_movimiento")
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
    patron = Pluck(PatronSchema(session=db.session), "nombre", dump_only=True)
    urlVideo = auto_field("url_video")
    pesoInicial = auto_field("peso_inicial")
    esTemporal = auto_field("es_temporal")
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
    patron = Nested(PatronSchema(session=db.session))
    urlVideo = auto_field("url_video")
    pesoInicial = auto_field("peso_inicial")
    esTemporal = auto_field("es_temporal")


# SCHEMA para PUT de ejercicio. Creo uno nuevo porque en los otros esta pluckeado el patron
# Y si lo paso a Nested, el cambio deberia "romper" las aplicaciones.
class EjercicioPutSchema(SQLAlchemySchema):
    class Meta:
        model = Ejercicio
        load_instance = True
        unknown = EXCLUDE

    idEjercicio = auto_field("id_ejercicio")
    nombre = auto_field(required=True)
    patron = Nested(PatronSchema(session=db.session))
    urlVideo = auto_field("url_video")
    pesoInicial = auto_field("peso_inicial")
    esTemporal = auto_field("es_temporal")
