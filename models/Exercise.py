from datetime import datetime
from app import db


class Exercise(db.Model):
    __tablename__ = 'exercises'
    __table_args__ = {"schema": "lacucha"}

    id_exercise = db.Column(db.Integer, db.Sequence(
        'id_exercise_seq'), primary_key=True, unique=True)
    name = db.Column(db.String())
    zone = db.Column(db.String())
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=None)

    def __init__(self, name, zone):
        self.name = name
        self.zone = zone

    def __repr__(self):
        return '<Exercise {}>'.format(self.id_exercise)

    def to_json(self):
        return {
            "id": self.id_exercise,
            "name": self.name,
            "zone": self.zone,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at
        }
