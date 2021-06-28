from app.mesociclos.model import Objetivo, Organizacion
from datetime import datetime
from typing import List
from app import db
from app.usuarios.model import Nivel
from app.sesiones.model import Sesion


class Plantilla(db.Model):
    __tablename__ = "plantillas"

    id_plantilla = db.Column(
        db.Integer,
        db.Sequence("plantillas_id_plantilla_seq"),
        primary_key=True,
        unique=True,
    )
    sesiones = db.relationship(
        "SesionXPlantilla",
        lazy="subquery",
        backref=db.backref("plantillas", lazy=True),
        order_by="SesionXPlantilla.id_sesionesxplantilla",
        cascade="all, delete-orphan",
    )
    nombre = db.Column(db.String(100))
    id_nivel = db.Column(db.Integer, db.ForeignKey("niveles.id_nivel"))
    nivel = db.relationship("Nivel", uselist=False)
    id_objetivo = db.Column(db.Integer, db.ForeignKey("objetivos.id_objetivo"))
    objetivo = db.relationship("Objetivo", uselist=False)
    id_organizacion = db.Column(
        db.Integer, db.ForeignKey("organizaciones.id_organizacion")
    )
    organizacion = db.relationship("Organizacion", uselist=False)
    sesiones_por_semana = db.Column(db.Integer)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    actualizado_en = db.Column(db.DateTime, default=None)

    def __init__(
        self,
        nombre: str,
        sesiones: List[Sesion],
        nivel: Nivel,
        objetivo: Objetivo,
        organizacion: Organizacion,
        sesiones_por_semana: int,
    ):
        self.sesiones = sesiones
        self.nombre = nombre
        self.nivel = nivel
        self.objetivo = objetivo
        self.organizacion = organizacion
        self.sesiones_por_semana = sesiones_por_semana

    def __repr__(self):
        return "<Plantilla {}>".format(self.id_plantilla)

    def to_json(self):
        return {
            "id": self.id_plantilla,
            "sesiones": [sesion.to_json() for sesion in self.sesion],
            "organizacion": self.organizacion.descripcion,
            "objetivo": self.objetivo.descripcion,
            "nivel": self.nivel.descripcion,
            "sesionesPorSemana": str(self.sesiones_por_semana),
            "creadoEn": self.creado_en,
            "actualizadoEn": self.actualizdo_en,
        }


class SesionXPlantilla(db.Model):
    __tablename__ = "sesionesxplantilla"

    id_sesionesxplantilla = db.Column(
        db.Integer,
        db.Sequence("sesionesxplantilla_id_sesionesxplantilla_seq"),
        primary_key=True,
        unique=True,
    )
    id_sesion = db.Column(db.Integer, db.ForeignKey("sesiones.id_sesion"))
    id_plantilla = db.Column(db.Integer, db.ForeignKey("plantillas.id_plantilla"))
    sesion = db.relationship("Sesion", uselist=False, cascade="all")

    def __init__(self, sesion):
        self.sesion = sesion

    def __repr__(self):
        return "<SesionXPlantilla {}>".format(self.id_sesionesxplantilla)

    def to_json(self):
        return {
            "id": self.id_sesionesxplantilla,
        }
