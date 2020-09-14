from app.sesiones.schema import SesionSchema
from app.ejercicios.schema import EjercicioSchema
from marshmallow import Schema, fields


class MesocicloSchema(Schema):
    id = fields.Int(dump_only=True)
    usuario = fields.Str(required=True)
    nivel = fields.Str(required=True)
    objetivo = fields.Str(required=True)
    organizacion = fields.Str(required=True)
    principal_tren_superior = fields.Str(required=True)  # Nombre del ejercicio
    principal_tren_inferior = fields.Str(required=True)  # Nombre del ejercicio
    semanas_por_mesociclo = fields.Int(required=True)
    sesiones_por_semana = fields.Int(required=True)
    sesiones = fields.List(fields.Nested(SesionSchema()))


class FinMesocicloSchema(Schema):
    id = fields.Int(dump_only=True)
    fecha_fin_real = fields.DateTime(required=True)
    aumento_motivacion = fields.Boolean()
    mas_cerca_objetivos = fields.Boolean()
    sentimiento = fields.Int()
    durmiendo = fields.Int()
    alimentado = fields.Int()
