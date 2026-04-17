from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint

db = SQLAlchemy()

class Exercise(db.Model):
    __tablename__ = 'exercises'
    # Layer 1: Table Constraint (Name length)
    __table_args__ = (CheckConstraint('length(name) >= 3', name='name_min_length'),)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    category = db.Column(db.String)
    equipment_needed = db.Column(db.Boolean, default=False)
    
    workout_exercises = db.relationship('WorkoutExercise', back_populates='exercise', cascade="all, delete-orphan")

    # Layer 2: Model Validation
    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name) < 3:
            raise ValueError("Exercise name must be at least 3 characters long.")
        return name

class Workout(db.Model):
    __tablename__ = 'workouts'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    duration_minutes = db.Column(db.Integer)
    notes = db.Column(db.Text)
    
    workout_exercises = db.relationship('WorkoutExercise', back_populates='workout', cascade="all, delete-orphan")

    @validates('duration_minutes')
    def validate_duration(self, key, duration):
        if duration and duration <= 0:
            raise ValueError("Duration must be a positive integer.")
        return duration

class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'
    # Layer 1: Table Constraint (Reps cannot be negative)
    __table_args__ = (CheckConstraint('reps >= 0', name='reps_positive'),)
    
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    workout = db.relationship('Workout', back_populates='workout_exercises')
    exercise = db.relationship('Exercise', back_populates='workout_exercises')