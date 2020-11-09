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

    idEstadoMesociclo = auto_field("id_estado_mesociclo")
    descripcion = auto_field(dump_only=True)


class ObjetivoSchema(SQLAlchemySchema):
    class Meta:
        model = Objetivo
        load_instance = True

    idObjetivo = auto_field("id_objetivo")
    descripcion = auto_field(dump_only=True)


class OrganizacionSchema(SQLAlchemySchema):
    class Meta:
        model = Organizacion
        load_instance = True

    idOrganizacion = auto_field('id_organizacion')
    descripcion = auto_field(dump_only=True)


class MesocicloSchema(SQLAlchemySchema):
    class Meta:
        model = Mesociclo
        load_instance = True

    idMesociclo = auto_field("id_mesociclo")
    usuario = Nested(UsuarioSchema(session=db.session), required=True)
    estado = Nested(EstadoMesocicloSchema(session=db.session), dump_only=True)
    nivel = Nested(NivelSchema(session=db.session), required=True)
    objetivo = Nested(ObjetivoSchema(session=db.session), required=True)
    organizacion = Nested(OrganizacionSchema(
        session=db.session), required=True)
    principalTrenSuperior = Nested(
        EjercicioSchema(session=db.session), attribute='principal_tren_superior', required=True)
    principalTrenInferior = Nested(
        EjercicioSchema(session=db.session), attribute='principal_tren_inferior', required=True)
    semanasPorMesociclo = auto_field("semanas_por_mesociclo", required=True)
    sesionesPorSemana = auto_field("sesiones_por_semana", required=True)
    sesiones = List(Nested(SesionSchema(session=db.session), required=True))
    fechaFinReal = auto_field("fecha_fin_real", dump_only=True)
    aumentoMotivacion = auto_field("aumento_motivacion", dump_only=True)
    masCercaObjetivos = auto_field("mas_cerca_objetivos", dump_only=True)
    sentimiento = auto_field(dump_only=True)
    durmiendo = auto_field(dump_only=True)
    alimentado = auto_field(dump_only=True)
    creadoEn = auto_field("creado_en", dump_only=True)
    actualizadoEn = auto_field("actualizado_en", dump_only=True)


class MesocicloUpdateSchema(SQLAlchemySchema):
    class Meta:
        model = Mesociclo
        load_instance = True

    idMesociclo = auto_field("id_mesociclo", required=True)
    usuario = Nested(UsuarioSchema(session=db.session))
    estado = Nested(EstadoMesocicloSchema(session=db.session))
    nivel = Nested(NivelSchema(session=db.session))
    objetivo = Nested(ObjetivoSchema(session=db.session))
    organizacion = Nested(OrganizacionSchema(session=db.session))
    principalTrenSuperior = Nested(EjercicioSchema(
        session=db.session), attribute='principal_tren_superior')
    principalTrenInferior = Nested(EjercicioSchema(
        session=db.session), attribute='principal_tren_inferior')
    semanasPorMesociclo = auto_field("semanas_por_mesociclo", required=False)
    sesionesPorSemana = auto_field("sesiones_por_semana", required=False)
    sesiones = List(Nested(SesionSchema(session=db.session)))
    fechaFinReal = auto_field("fecha_fin_real")
    aumentoMotivacion = auto_field("aumento_motivacion")
    masCercaObjetivos = auto_field("mas_cerca_objetivos")
    sentimiento = auto_field()
    durmiendo = auto_field()
    alimentado = auto_field()
