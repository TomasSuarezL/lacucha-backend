from typing import List
from app.bloques.model import EjercicioXBloque
from datetime import datetime
from app import db


class Sesion(db.Model):
    __tablename__ = 'sesiones'

    id_sesion = db.Column(db.Integer, db.Sequence(
        'sesion_id_sesion_seq'), primary_key=True, unique=True)
    id_mesociclo = db.Column(db.Integer, db.ForeignKey(
        'mesociclos.id_mesociclo', ondelete="cascade"), nullable=True)
    bloques = db.relationship(
        'Bloque', lazy='subquery', backref=db.backref('sesiones', lazy=True))
    fecha_empezado = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_finalizado = db.Column(db.DateTime, default=None)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    actualizado_en = db.Column(db.DateTime, default=None)

    def __init__(self, bloques: List[EjercicioXBloque], fecha_empezado: datetime, fecha_finalizado: datetime):
        self.bloques = bloques
        self.fecha_empezado = fecha_empezado
        self.fecha_finalizado = fecha_finalizado

    def __repr__(self):
        return '<Sesion {}>'.format(self.id_sesion)

    def to_json(self):
        return {
            "id": self.id_sesion,
            "mesociclo": self.id_mesociclo,
            "bloques": [bloque.to_json() for bloque in self.bloques],
            "startedAt": self.fecha_empezado,
            "finishedAt": self.fecha_finalizado,
            "createdAt": self.creado_en,
            "updatedAt": self.actualizado_en
        }
