#!/usr/bin/env python3
from app import app
from models import db, Exercise, Workout, WorkoutExercise

with app.app_context():
    print("Clearing database...")
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    print("Seeding exercises...")
    e1 = Exercise(name="Pushups", category="Strength")
    e2 = Exercise(name="Running", category="Cardio")
    db.session.add_all([e1, e2])
    db.session.commit()

    print("Seeding workout...")
    w1 = Workout(date="2023-10-25", duration_minutes=45, notes="Initial seed session")
    db.session.add(w1)
    db.session.commit()

    print("Linking first exercise...")
    we = WorkoutExercise(workout_id=w1.id, exercise_id=e1.id, reps=15, sets=3)
    db.session.add(we)
    db.session.commit()
    
    print("Seeding complete!")