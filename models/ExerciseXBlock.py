from datetime import datetime
from app import db


class ExerciseXBlock(db.Model):
    __tablename__ = 'exercisesxblock'
    __table_args__ = {"schema": "lacucha"}

    id_exercisexblock = db.Column(db.Integer, db.Sequence(
        "id_exercisexblock_seq"), primary_key=True, unique=True)
    id_exercise = db.Column(db.Integer, db.ForeignKey(
        'lacucha.exercises.id_exercise'))
    id_block = db.Column(db.Integer, db.ForeignKey('lacucha.blocks.id_block'))
    exercise = db.relationship("Exercise", uselist=False)
    block = db.relationship("Block", uselist=False)
    repetitions = db.Column(db.Integer)
    weight = db.Column(db.Float)

    def __init__(self, exercise, repetitions, weight):
        self.exercise = exercise
        self.repetitions = repetitions
        self.weight = weight

    def __repr__(self):
        return '<ExerciseXBlock {}>'.format(self.id_exercisexblock)

    def to_json(self):
        return {
            "id": self.id_exercisexblock,
            "exercise": self.exercise.name,
            "zone": self.exercise.zone,
            "load": self.weight,
            "reps": self.repetitions,
        }
