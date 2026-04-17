# workout-application-backend
A robust backend API built for personal trainers to track workouts and associated exercises. This application demonstrates a many-to-many relationship using Flask, SQLAlchemy, and Marshmallow.

## Features
- **Triple-Layer Validation**: Database constraints, SQLAlchemy model validations, and Marshmallow schema integrity.
- **Many-to-Many Relationships**: Exercises can be added to multiple workouts with unique sets/reps/duration.
- **RESTful Endpoints**: Full support for viewing, creating, and deleting workouts and exercises.
- **Serialization**: Nested data handling to show associated exercises within workout details.

## Technologies Used
- **Flask** (v2.2.2)
- **SQLAlchemy** (v3.0.3)
- **Marshmallow** (v3.20.1)
- **Flask-Migrate** (v3.1.0)
- **SQLite**

## Installation Instructions

1. **Clone the repository**
   ```bash
   git clone <your-github-link>
   cd SQLalchemy-summative-lab/workout_app


Install Dependencies
bash
pipenv install
pipenv shell
Use code with caution.

Initialize Database
bash
cd server
export FLASK_APP=app.py
flask db init
flask db migrate -m "Initial migration"
flask db upgrade head
Use code with caution.

Seed the Database
bash
python seed.py
Use code with caution.

Running the Application
From the server/ directory:
bash
python app.py
Use code with caution.

The server will start at http://127.0.0.1:5555.
API Endpoints

Workouts
GET /workouts - List all workouts.
GET /workouts/<id> - Show a single workout with its associated exercises.
POST /workouts - Create a new workout.
DELETE /workouts/<id> - Delete a workout (and its associated links).
Exercises

GET /exercises - List all exercises.
POST /exercises - Create a new exercise (requires name min 3 chars).
Workout Exercises (Relationships)
POST /workouts/<w_id>/add-exercises/<e_id> - Link an exercise to a workout with sets and reps.
Validations Implemented
Table Constraints: CheckConstraints ensure reps are non-negative and names have minimum lengths.
Model Validations: @validates hooks in SQLAlchemy ensure data logic (e.g., positive duration).
Schema Validations: Marshmallow validates incoming JSON data types and lengths before processing.
