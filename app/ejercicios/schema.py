from marshmallow import Schema, fields


class EjercicioSchema(Schema):
    id_ejercicio = fields.Int(dump_only=True)
    nombre = fields.Str(required=True)
    patron = fields.Str(dump_only=True)
    creado_en = fields.DateTime(dump_only=True)
    actualizado_en = fields.DateTime(dump_only=True)
