from datetime import datetime
from app import db


class Bloque(db.Model):
    __tablename__ = 'bloques'

    id_bloques = db.Column(db.Integer, db.Sequence(
        'bloques_id_bloques_seq'), primary_key=True, unique=True)
    id_sesiones = db.Column(db.Integer, db.ForeignKey(
        'sesiones.id_sesiones', ondelete="cascade"), nullable=False)
    ejercicios = db.relationship(
        'EjercicioXBloque', lazy='subquery', backref=db.backref('bloques', lazy=True))
    num_bloque = db.Column(db.Integer)
    series = db.Column(db.Integer)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    actualizdo_en = db.Column(db.DateTime, default=None)

    def __init__(self, ejercicios, num_bloque, series):
        self.ejercicios = ejercicios
        self.num_bloque = num_bloque
        self.series = series

    def __repr__(self):
        return '<Bloque {}>'.format(self.id_bloques)

    def to_json(self):
        return {
            "id": self.id_bloque,
            "ejercicios": [ejercicio.to_json() for ejercicio in self.ejercicios],
            "numBloque": self.num_bloque,
            "series": self.series,
            "creadoEn": self.creado_en,
            "actualizadoEn": self.actualizdo_en
        }


class EjercicioXBloque(db.Model):
    __tablename__ = 'ejerciciosxbloque'

    id_ejerciciosxbloque = db.Column(db.Integer, db.Sequence(
        "ejerciciosxbloque_id_ejerciciosxbloque_seq"), primary_key=True, unique=True)
    id_ejercicio = db.Column(db.Integer, db.ForeignKey(
        'ejercicios.id_ejercicio'))
    id_bloque = db.Column(db.Integer, db.ForeignKey('bloques.id_bloques'))
    ejercicio = db.relationship("Ejercicio", uselist=False)
    bloque = db.relationship("Bloque", uselist=False)
    repeticiones = db.Column(db.Integer)
    carga = db.Column(db.Float)

    def __init__(self, ejercicio, repeticiones, carga):
        self.ejercicio = ejercicio
        self.repeticiones = repeticiones
        self.carga = carga

    def __repr__(self):
        return '<EjercicioXBloque {}>'.format(self.id_ejerciciosxbloque)

    def to_json(self):
        return {
            "id": self.id_ejercicioxbloque,
            "ejercicio": self.ejercicio.nombre,
            "patron": self.ejercicio.patron.nombre,
            "carga": self.carga,
            "repeticiones": self.repeticiones,
        }
