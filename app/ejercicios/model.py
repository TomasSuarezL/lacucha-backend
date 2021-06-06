from datetime import datetime

from sqlalchemy.orm import backref
from app import db


class PatronMovimiento(db.Model):
    __tablename__ = "patrones_movimiento"

    id_patron_movimiento = db.Column(
        db.Integer,
        db.Sequence("patrones_movimiento_id_patron_movimiento_seq"),
        primary_key=True,
        unique=True,
    )
    nombre = db.Column(db.String())
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    actualizado_en = db.Column(db.DateTime, default=None)

    def __init__(self, nombre):
        self.nombre = nombre

    def __repr__(self):
        return "<PatronMovimiento {}>".format(self.id_patron_movimiento)

    def to_json(self):
        return {
            "id": self.id_patron_movimiento,
            "nombre": self.nombre,
            "creado_en": self.creado_en,
            "actualizado_en": self.actualizado_en,
        }


class Ejercicio(db.Model):
    __tablename__ = "ejercicios"

    id_ejercicio = db.Column(
        db.Integer,
        db.Sequence("ejercicios_id_ejercicio_seq"),
        primary_key=True,
        unique=True,
    )
    nombre = db.Column(db.String())
    id_patron = db.Column(
        db.Integer, db.ForeignKey("patrones_movimiento.id_patron_movimiento")
    )
    patron = db.relationship(
        "PatronMovimiento",
        uselist=False,
        lazy=True,
        backref=db.backref("ejercicios", lazy=True),
    )
    url_video = db.Column(db.String())
    peso_inicial = db.Column(db.Integer)
    es_temporal = db.Column(db.Boolean)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    actualizado_en = db.Column(db.DateTime, default=None)

    def __init__(
        self, nombre, patron=None, url_video=None, peso_inicial=0, es_temporal=0
    ):
        self.nombre = nombre
        self.patron = patron
        self.url_video = url_video
        self.peso_inicial = peso_inicial
        self.es_temporal = es_temporal

    def __repr__(self):
        return "<Ejercicio {}>".format(self.id_ejercicio)

    def to_json(self):
        return {
            "id": self.id_ejercicio,
            "nombre": self.nombre,
            "patron": self.patron.nombre,
            "url_video": self.url_video,
            "peso_inicial": self.peso_inicial,
            "es_temporal": self.es_temporal,
            "creado_en": self.creado_en,
            "actualizado_en": self.actualizado_en,
        }
