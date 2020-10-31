from app.usuarios.schema import NivelSchema, UsuarioSchema
from app.ejercicios.schema import EjercicioSchema
from marshmallow.fields import List, Nested
from marshmallow_sqlalchemy.schema.sqlalchemy_schema import SQLAlchemySchema, auto_field
from app import db
from app.mesociclos.model import EstadoMesociclo, Mesociclo, Objetivo, Organizacion
from app.sesiones.schema import SesionSchema


class EstadoMesocicloSchema(SQLAlchemySchema):
    class Meta:
        model = EstadoMesociclo
        load_instance = True

    id_estado_mesociclo = auto_field()
    descripcion = auto_field()


class ObjetivoSchema(SQLAlchemySchema):
    class Meta:
        model = Objetivo
        load_instance = True

    id_objetivo = auto_field()
    descripcion = auto_field()


class OrganizacionSchema(SQLAlchemySchema):
    class Meta:
        model = Organizacion
        load_instance = True

    id_organizacion = auto_field()
    descripcion = auto_field()


class MesocicloSchema(SQLAlchemySchema):
    class Meta:
        model = Mesociclo
        load_instance = True

    id_mesociclo = auto_field()
    usuario = auto_field(required=True)
    estado = auto_field()
    nivel = auto_field(required=True)
    objetivo = auto_field(required=True)
    organizacion = auto_field(required=True)
    principal_tren_superior = auto_field(required=True)  # Nombre del ejercicio
    principal_tren_inferior = auto_field(required=True)  # Nombre del ejercicio
    semanas_por_mesociclo = auto_field(required=True)
    sesiones_por_semana = auto_field(required=True)
    sesiones = List(Nested(SesionSchema(session=db.session)))
    fechaFinReal = auto_field("fecha_fin_real")
    aumentoMotivacion = auto_field("aumento_motivacion")
    masCercaObjetivos = auto_field("mas_cerca_objetivos")
    sentimiento = auto_field()
    durmiendo = auto_field()
    alimentado = auto_field()


class MesocicloFlatSchema(SQLAlchemySchema):
    class Meta:
        model = Mesociclo
        load_instance = True

    id_mesociclo = auto_field()
    usuario = Nested(UsuarioSchema(session=db.session))
    estado = Nested(EstadoMesocicloSchema(session=db.session))
    nivel = Nested(NivelSchema(session=db.session))
    objetivo = Nested(ObjetivoSchema(session=db.session))
    organizacion = Nested(OrganizacionSchema(session=db.session))
    principal_tren_superior = Nested(EjercicioSchema(
        session=db.session))   # Nombre del ejercicio
    principal_tren_inferior = Nested(EjercicioSchema(
        session=db.session))  # Nombre del ejercicio
    semanas_por_mesociclo = auto_field(required=True)
    sesiones_por_semana = auto_field(required=True)
    sesiones = List(Nested(SesionSchema(session=db.session)))
    fechaFinReal = auto_field("fecha_fin_real")
    aumentoMotivacion = auto_field("aumento_motivacion")
    masCercaObjetivos = auto_field("mas_cerca_objetivos")
    sentimiento = auto_field()
    durmiendo = auto_field()
    alimentado = auto_field()
