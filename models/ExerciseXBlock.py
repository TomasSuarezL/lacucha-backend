from app import db

exerciseXblock = db.Table('exercisesxblock',
                          db.Column('id_exercise', db.Integer, db.ForeignKey(
                              'lacucha.exercises.id_exercise'), primary_key=True),
                          db.Column('id_block', db.Integer, db.ForeignKey(
                              'lacucha.blocks.id_block'), primary_key=True),
                          db.Column('repetitions', db.Integer),
                          db.Column('weight', db.Float), schema="lacucha")
