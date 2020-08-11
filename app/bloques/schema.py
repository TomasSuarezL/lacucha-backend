from marshmallow.utils import EXCLUDE
from app.bloques.model import EjercicioXBloque
from app.ejercicios.schema import EjercicioSchema
from marshmallow import Schema, fields, post_load


class EjercicioXBloqueSchema(Schema):
    id = fields.Int(dump_only=True)
    ejercicio = fields.Nested(EjercicioSchema(unknown=EXCLUDE))
    repeticiones = fields.Int(required=True)
    carga = fields.Float(required=True)


class BloqueSchema(Schema):
    id = fields.Int(dump_only=True)
    series = fields.Int(required=True)
    numBloque = fields.Int(required=True)
    ejercicios = fields.List(fields.Nested(EjercicioXBloqueSchema()))
