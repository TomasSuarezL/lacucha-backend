from datetime import datetime
from app import db
from .ExerciseXBlock import exerciseXblock


class Block(db.Model):
    __tablename__ = 'blocks'
    __table_args__ = {"schema": "lacucha"}

    id_block = db.Column(db.Integer, db.Sequence(
        'id_block_seq'), primary_key=True, unique=True)
    sessionid = db.Column(db.Integer, db.ForeignKey(
        'lacucha.sessions.id_session'), nullable=False)
    exercises = db.relationship(
        'Exercise', secondary=exerciseXblock, lazy='subquery', backref=db.backref('blocks', lazy=True))
    block_num = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=None)

    def __init__(self, exercises, block_num, sets):
        self.exercises = exercises
        self.block_num = block_num
        self.sets = sets

    def __repr__(self):
        return '<Block {}>'.format(self.id_block)

    def to_json(self):
        return {
            "id": self.id_block,
            "blocks": [exercise.to_json() for exercise in self.exercises],
            "block_num": self.block_num,
            "sets": self.sets,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
