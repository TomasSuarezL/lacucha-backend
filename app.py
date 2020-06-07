import os
import config
from datetime import date
from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from cerberus import Validator

app = Flask(__name__)
app.config.from_object(config.DevelopmentConfig)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)
db = SQLAlchemy(app)


# NEW POST SCHEMA VALIDATION FOR REQUEST BODY.
exerciseSchema = {
    'type': 'dict',
    'schema': {
        "name": {'type': 'string', 'required': True},
        "zone": {'type': 'string', 'required': False},
        "load": {'type': 'float', 'required': False},
        "reps": {'type': 'integer', 'required': True}
    }
}

blockSchema = {
    'type': 'dict',
    'schema': {
        'blockNum': {'type': 'integer', 'required': True},
        'sets': {'type': 'integer', 'required': True},
        "exercises": {'type': 'list', 'schema': exerciseSchema}
    }
}

sessionSchema = {
    'startedAt': {'type': 'string', 'required': True},
    'finishedAt': {'type': 'string', 'required': True},
    'blocks': {'type': 'list', 'schema': blockSchema},
}

sessionValidator = Validator(sessionSchema)


@app.route('/')
def index():
    result = db.session.execute('SELECT 1')
    print(result)
    return "Ok"


@app.route('/sessions', methods=['GET', 'POST'])
def sessions():
    if request.method == 'POST':
        from models import Session, Block, Exercise, ExerciseXBlock

        bodySession = request.get_json(force=True)

        try:
            # Validate body of request
            if(not sessionValidator.validate(bodySession, sessionSchema)):
                abort(
                    400, f"Invalid Body. Errors: {str(sessionValidator.errors)} \n post schema: {str(sessionSchema)}")

            blocks = [Block(exercises=[ExerciseXBlock(exercise=Exercise.query.filter_by(name=exercise.get("name")).first(), weight=exercise.get("load"), repetitions=exercise.get("reps")) for exercise in block.get('exercises')], block_num=block.get(
                'blockNum'), sets=block.get('sets')) for block in bodySession.get('blocks')]

            session = Session(blocks=blocks, started_at=bodySession.get(
                'startedAt'), finished_at=bodySession.get('finishedAt'))

            db.session.add(session)
            db.session.commit()

            return "Session Created", 200
        except AttributeError as err:
            print(err)
            return err, 400
        except:
            return 400

    else:
        from models import Session
        sessions = Session.query.order_by(Session.created_at.desc()).all()
        return jsonify([ses.to_json() for ses in sessions])


@app.route('/todaySession', methods=['GET'])
def todaySession():
    from models import Session
    session = Session.query.filter(Session.created_at >= date.today(
    )).order_by(Session.created_at.desc()).first()
    return jsonify(session.to_json() if session != None else session)


@app.route('/exercises', methods=['GET', 'POST'])
def exercises():
    if request.method == 'POST':
        return "Not implemented yet"
    else:
        from models import Exercise
        _zone = request.args.get('zone', None)
        exercises = Exercise.query.filter_by(zone=_zone).all()
        return jsonify([ex.to_json() for ex in exercises])
