import re
from marshmallow import Schema, fields


class UsuarioSchema(Schema):
    id_usuario = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Str(required=True)
    nombre = fields.Str(required=True)
    apelliduo = fields.Str(required=True)
    fecha_nacimiento = fields.Str(required=True)
    genero = fields.Str(required=True)
    altura = fields.Float(required=True)
    peso = fields.Float(required=True)
    nivel = fields.Str(required=True)
    creado_en = fields.DateTime(dump_only=True)
    actualizado_en = fields.DateTime(dump_only=True)
