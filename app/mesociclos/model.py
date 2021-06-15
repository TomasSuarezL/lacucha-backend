from app.sesiones.model import Sesion
from typing import List
from app.usuarios.model import Nivel, Usuario
from app.ejercicios.model import Ejercicio
from datetime import datetime
from app import db


class EstadoMesociclo(db.Model):
    __tablename__ = "estados_mesociclo"

    id_estado_mesociclo = db.Column(
        db.Integer,
        db.Sequence("estados_mesociclo_id_estados_mesociclo_seq"),
        primary_key=True,
        unique=True,
    )
    descripcion = db.Column(db.String(100), nullable=False, unique=True)

    def __init__(self, descripcion: str):
        self.descripcion = descripcion

    def __repr__(self):
        return "<EstadoMesociclo {}: {}>".format(
            self.id_estados_mesociclo, self.descripcion
        )


class Objetivo(db.Model):
    __tablename__ = "objetivos"

    id_objetivo = db.Column(
        db.Integer,
        db.Sequence("objetivos_id_objetivo_seq"),
        primary_key=True,
        unique=True,
    )
    descripcion = db.Column(db.String(100), nullable=False, unique=True)

    def __init__(self, descripcion: str):
        self.descripcion = descripcion

    def __repr__(self):
        return "<Objetivo {}: {}>".format(self.id_objetivo, self.descripcion)


class Organizacion(db.Model):
    __tablename__ = "organizaciones"

    id_organizacion = db.Column(
        db.Integer,
        db.Sequence("organizaciones_id_organizacion_seq"),
        primary_key=True,
        unique=True,
    )
    descripcion = db.Column(db.String(100), nullable=False, unique=True)

    def __init__(self, descripcion: str):
        self.descripcion = descripcion

    def __repr__(self):
        return "<Organizacion {}: {}>".format(self.id_organizacion, self.descripcion)


class Mesociclo(db.Model):
    __tablename__ = "mesociclos"

    id_mesociclo = db.Column(
        db.Integer,
        db.Sequence("mesociclos_id_mesociclo_seq"),
        primary_key=True,
        unique=True,
    )
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id_usuario"))
    usuario = db.relationship("Usuario", uselist=False)
    id_nivel = db.Column(db.Integer, db.ForeignKey("niveles.id_nivel"))
    nivel = db.relationship("Nivel", uselist=False)
    id_estado = db.Column(
        db.Integer, db.ForeignKey("estados_mesociclo.id_estado_mesociclo"), default=1
    )  # default value = 1 "activo"
    estado = db.relationship("EstadoMesociclo", uselist=False)
    id_objetivo = db.Column(db.Integer, db.ForeignKey("objetivos.id_objetivo"))
    objetivo = db.relationship("Objetivo", uselist=False)
    id_organizacion = db.Column(
        db.Integer, db.ForeignKey("organizaciones.id_organizacion")
    )
    organizacion = db.relationship("Organizacion", uselist=False)
    id_principal_tren_superior = db.Column(
        db.Integer, db.ForeignKey("ejercicios.id_ejercicio")
    )
    principal_tren_superior = db.relationship(
        "Ejercicio", foreign_keys=[id_principal_tren_superior], uselist=False
    )
    id_principal_tren_inferior = db.Column(
        db.Integer, db.ForeignKey("ejercicios.id_ejercicio")
    )
    principal_tren_inferior = db.relationship(
        "Ejercicio", foreign_keys=[id_principal_tren_inferior], uselist=False
    )
    semanas_por_mesociclo = db.Column(db.Integer, nullable=False)
    sesiones_por_semana = db.Column(db.Integer, nullable=False)
    sesiones = db.relationship(
        "Sesion",
        lazy="subquery",
        backref=db.backref("mesociclo", lazy=True),
        order_by="Sesion.num_sesion",
    )
    # Fin de mesociclo
    fecha_fin_real = db.Column(db.DateTime, default=None)
    aumento_motivacion = db.Column(db.Boolean, default=None)
    mas_cerca_objetivos = db.Column(db.Boolean, default=None)
    # del 1 al 10 o 1 al 5, como te sentiste este mesociclo? no obligatorio
    sentimiento = db.Column(db.Integer, default=None)
    # del 1 al 10 o 1 al 5, como dormiste este mesociclo? no obligatorio
    durmiendo = db.Column(db.Integer, default=None)
    # del 1 al 10 o 1 al 5, como te alimentaste este mesociclo? no obligatorio
    alimentado = db.Column(db.Integer, default=None)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    actualizado_en = db.Column(db.DateTime, default=None)

    def __init__(
        self,
        usuario: Usuario,
        nivel: Nivel,
        objetivo: Objetivo,
        organizacion: Organizacion,
        principal_tren_superior: Ejercicio,
        principal_tren_inferior: Ejercicio,
        semanas_por_mesociclo: int,
        sesiones_por_semana: int,
        sesiones: List[Sesion],
    ):

        self.usuario = usuario
        self.nivel = nivel
        self.objetivo = objetivo
        self.organizacion = organizacion
        self.principal_tren_superior = principal_tren_superior
        self.principal_tren_inferior = principal_tren_inferior
        self.semanas_por_mesociclo = semanas_por_mesociclo
        self.sesiones_por_semana = sesiones_por_semana
        self.sesiones = sesiones

        self.estado = EstadoMesociclo.query.get(1)

    def __repr__(self):
        return "<Mesociclo {}>".format(self.id_mesociclo)

    def to_json(self):
        return {
            "id": self.id_mesociclo,
        }
