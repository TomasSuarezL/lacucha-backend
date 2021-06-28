from marshmallow.fields import List, Nested
from marshmallow.utils import EXCLUDE
from marshmallow_sqlalchemy.schema.sqlalchemy_schema import SQLAlchemySchema, auto_field
from app import db
from app.plantillas.model import SesionXPlantilla, Plantilla
from app.mesociclos.schema import ObjetivoSchema, OrganizacionSchema
from app.sesiones.schema import SesionSchema
from app.usuarios.schema import NivelSchema


class SesionXPlantillaSchema(SQLAlchemySchema):
    class Meta:
        model = SesionXPlantilla
        load_instance = True
        unknown = EXCLUDE

    idSesionesxplantilla = auto_field("id_sesionesxplantilla")
    sesion = Nested(SesionSchema(session=db.session, unknown=EXCLUDE))


class PlantillaSchema(SQLAlchemySchema):
    class Meta:
        model = Plantilla
        load_instance = True
        unknown = EXCLUDE

    idPlantilla = auto_field("id_plantilla")
    sesiones = List(Nested(SesionXPlantillaSchema(session=db.session)))
    nombre = auto_field("nombre")
    nivel = Nested(NivelSchema(session=db.session))
    objetivo = Nested(ObjetivoSchema(session=db.session))
    organizacion = Nested(OrganizacionSchema(session=db.session))
    sesionesPorSemana = auto_field("sesiones_por_semana", required=True)
    creadoEn = auto_field("creado_en", dump_only=True)
    actualizadoEn = auto_field("actualizado_en", dump_only=True)

