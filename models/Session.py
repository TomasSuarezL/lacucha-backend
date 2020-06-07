from datetime import datetime
from app import db


class Session(db.Model):
    __tablename__ = 'sessions'
    __table_args__ = {"schema": "lacucha"}

    id_session = db.Column(db.Integer, db.Sequence(
        'id_session_seq'), primary_key=True, unique=True)
    blocks = db.relationship(
        'Block', lazy='subquery', backref=db.backref('sessions', lazy=True))
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    finished_at = db.Column(db.DateTime, default=None)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=None)

    def __init__(self, blocks, started_at, finished_at):
        self.blocks = blocks
        self.started_at = started_at
        self.finished_at = finished_at

    def __repr__(self):
        return '<Session {}>'.format(self.id_session)

    def to_json(self):
        return {
            "id": self.id_session,
            "blocks": [block.to_json() for block in self.blocks],
            "startedAt": self.started_at,
            "finishedAt": self.finished_at,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at
        }
