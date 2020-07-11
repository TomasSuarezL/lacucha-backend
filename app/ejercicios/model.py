from datetime import datetime
from app import db


class Ejercicio(db.Model):
    __tablename__ = 'ejercicios'

    id_ejercicio = db.Column(db.Integer, db.Sequence(
        'ejercicios_id_ejercicio_seq'), primary_key=True, unique=True)
    nombre = db.Column(db.String())
    id_patron = db.Column(db.Integer, db.ForeignKey(
        'patrones_movimiento.id_patron_movimiento'))
    patron = db.relationship("PatronMovimiento", uselist=False)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    actualizado_en = db.Column(db.DateTime, default=None)

    def __init__(self, nombre, patron):
        self.nombre = nombre
        self.patron = patron

    def __repr__(self):
        return '<Ejercicio {}>'.format(self.id_ejercicio)

    def to_json(self):
        return {
            "id": self.id_ejercicio,
            "nombre": self.nombre,
            "patron": self.patron.nombre,
            "creado_en": self.creado_en,
            "actualizado_en": self.actualizado_en
        }


class PatronMovimiento(db.Model):
    __tablename__ = 'patrones_movimiento'

    id_patron_movimiento = db.Column(db.Integer, db.Sequence(
        'patrones_movimiento_id_patron_movimiento_seq'), primary_key=True, unique=True)
    nombre = db.Column(db.String())
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    actualizado_en = db.Column(db.DateTime, default=None)

    def __init__(self, nombre):
        self.nombre = nombre

    def __repr__(self):
        return '<PatronMovimiento {}>'.format(self.id_patron_movimiento)

    def to_json(self):
        return {
            "id": self.id_patron_movimiento,
            "nombre": self.nombre,
            "creado_en": self.creado_en,
            "actualizado_en": self.actualizado_en
        }
