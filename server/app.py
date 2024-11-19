# app.py - Backend server using Flask
from flask import Flask, jsonify, request, session
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app) 
app.secret_key = 'hi' 

# Connect to MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="test_root",
    database="logbook"
)

@app.route('/exercises', methods=['GET'])
def get_exercises():
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT ExerciseID, Name, Body_Part, Equipment FROM EXERCISES")
    exercises = cursor.fetchall()
    cursor.close()
    return jsonify(exercises)

@app.route('/workoutperformance', methods=['GET'])
def get_performance():
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM WORKOUT_PERFORMANCE, EXERCISES WHERE WORKOUT_PERFORMANCE.ExerciseID = EXERCISES.ExerciseID ORDER BY PerformanceID DESC;")
    performances = cursor.fetchall()
    cursor.close
    return jsonify(performances)

@app.route('/start-workout', methods=['POST'])
def start_workout():
    user_id = 1#get_active_user_id()
    if not user_id:
        return jsonify({"message": "User not logged in"}), 403

    cursor = mydb.cursor()

    cursor.execute("INSERT INTO WORKOUT (UserID) VALUES (%s)", (1,))
    mydb.commit()
    new_workout_id = cursor.lastrowid
    cursor.close()
    return jsonify({"message": "Workout started", "WorkoutID": new_workout_id}), 201


@app.route('/add-or-get-exercise', methods=['POST'])
def add_or_get_exercise():
    data = request.json
    exercise_name = data.get("Name")
    body_part = data.get("Body_Part")
    equipment = data.get("Equipment")

    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT ExerciseID FROM EXERCISES WHERE Name = %s", (exercise_name,))
    result = cursor.fetchone()
    print(result)
    if result:
        exercise_id = result["ExerciseID"]
    else:
        cursor.execute(
            "INSERT INTO EXERCISES (Name, Body_Part, Equipment) VALUES (%s, %s, %s)",
            (exercise_name, body_part, equipment)
        )
        mydb.commit()
        exercise_id = cursor.lastrowid

    cursor.close()
    return jsonify({"ExerciseID": exercise_id})


@app.route('/submit-workout-performance', methods=['POST'])
def submit_workout_performance():
    data = request.json
    print(data)
    workout_id = data.get("WorkoutID")
    exercise_id = data.get("ExerciseID")
    user_id = data.get("UserID")
    reps = data.get("Reps")
    set_number = data.get("Set_Number")
    rir = data.get("RIR")
    weight = data.get("Weight")  # New weight parameter
    print('hello')
    cursor = mydb.cursor()
    cursor.execute("""
        INSERT INTO WORKOUT_PERFORMANCE (WorkoutID, UserID, ExerciseID, Reps, Set_Number, RIR, Weight)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (workout_id, user_id, exercise_id, reps, set_number, rir, weight))
    mydb.commit()
    cursor.close()
    return jsonify({"message": "Workout performance submitted successfully"}), 201


@app.route('/workouts', methods=['POST'])
def add_workout():
    data = request.json

    WorkoutID = data.get('WorkoutID')
    UserID = 1 #data.get('UserID')            Add ability to add multiple users
    ExerciseID = data.get('ExerciseID')
    Reps = data.get('Reps')
    Sets = data.get('Sets')
    RepsInReserve = data.get('RIR')

    cursor = mydb.cursor()
    query = """
        INSERT INTO WORKOUT_PERFORMANCE (WorkoutID, UserID, ExerciseID, Reps, Sets, RepsInReserve)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (WorkoutID, UserID, ExerciseID, Reps, Sets, RepsInReserve))
    mydb.commit()
    cursor.close()


# User Sign-Up
@app.route('/sign-up', methods=['POST'])
def sign_up():
    data = request.json
    name = data.get("Name")
    
    cursor = mydb.cursor()
    cursor.execute("INSERT INTO users (Name) VALUES (%s)", (name,))
    mydb.commit()
    user_id = cursor.lastrowid
    cursor.close()

    return jsonify({"message": "User registered successfully", "UserID": user_id}), 201

# User Log-In
@app.route('/log-in', methods=['POST'])
def log_in():
    data = request.json
    name = data.get("Name")
    
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT UserID FROM users WHERE Name = %s", (name,))
    user = cursor.fetchone()
    cursor.close()
    
    if user:
        session['user_id'] = user["UserID"]  # Store active user in session
        return jsonify({"message": "Login successful", "UserID": user["UserID"]}), 200
    else:
        return jsonify({"message": "User not found"}), 404

# Logout route to clear the session
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({"message": "Logged out successfully"}), 200

# Access active user ID in other routes
def get_active_user_id():
    return session.get('user_id')  # Use this to access the logged-in user ID

if __name__ == '__main__':
    app.run(debug=True)
