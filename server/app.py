from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate
from marshmallow import Schema, fields, validate, ValidationError
from models import db, Exercise, Workout, WorkoutExercise
import os

app = Flask(__name__)
# Absolute path to avoid database mismatch issues
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

# --- MARSHMALLOW SCHEMAS (Validation Layer 3) ---

class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=3))
    category = fields.Str()
    equipment_needed = fields.Bool()

class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    reps = fields.Int(validate=validate.Range(min=0))
    sets = fields.Int(validate=validate.Range(min=0))
    duration_seconds = fields.Int()
    exercise = fields.Nested(ExerciseSchema, only=("name", "category"))

class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Str(required=True)
    duration_minutes = fields.Int()
    notes = fields.Str()
    workout_exercises = fields.List(fields.Nested(WorkoutExerciseSchema))

# Init Schemas
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
workout_ex_schema = WorkoutExerciseSchema()

# --- ROUTES ---

@app.route('/workouts', methods=['GET', 'POST'])
def workouts():
    if request.method == 'GET':
        return make_response(workouts_schema.dump(Workout.query.all()), 200)
    
    data = request.json
    new_workout = Workout(date=data.get('date'), duration_minutes=data.get('duration_minutes'), notes=data.get('notes'))
    db.session.add(new_workout)
    db.session.commit()
    return make_response(workout_schema.dump(new_workout), 201)

@app.route('/workouts/<int:id>', methods=['GET', 'DELETE'])
def workout_by_id(id):
    workout = Workout.query.get(id)
    if not workout:
        return make_response({"error": "Workout not found"}, 404)
    if request.method == 'GET':
        return make_response(workout_schema.dump(workout), 200)
    db.session.delete(workout)
    db.session.commit()
    return make_response({}, 204)

@app.route('/exercises', methods=['GET', 'POST'])
def exercises():
    if request.method == 'GET':
        return make_response(exercises_schema.dump(Exercise.query.all()), 200)
    
    data = request.json
    # Schema validation check
    errors = exercise_schema.validate(data)
    if errors:
        return make_response(errors, 400)
        
    new_ex = Exercise(name=data['name'], category=data.get('category'))
    db.session.add(new_ex)
    db.session.commit()
    return make_response(exercise_schema.dump(new_ex), 201)

# CUSTOM URL: Add exercise to workout
@app.route('/workouts/<int:w_id>/add-exercises/<int:e_id>', methods=['POST'])
def add_exercise_to_workout(w_id, e_id):
    data = request.json
    new_we = WorkoutExercise(
        workout_id=w_id,
        exercise_id=e_id,
        reps=data.get('reps'),
        sets=data.get('sets'),
        duration_seconds=data.get('duration_seconds')
    )
    db.session.add(new_we)
    db.session.commit()
    return make_response(workout_ex_schema.dump(new_we), 201)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=True)