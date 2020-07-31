from marshmallow import Schema, fields, post_load
from app.bloques.schema import BloqueSchema


class SesionSchema(Schema):
    id = fields.Int(dump_only=True)
    bloques = fields.List(fields.Nested(BloqueSchema()))
    empezado = fields.Str()
    finalizado = fields.Str()
