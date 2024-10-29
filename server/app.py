# app.py - Backend server using Flask
from flask import Flask, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app) 

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
    cursor.execute("SELECT Name, Body_Part, Equipment FROM EXERCISES")
    exercises = cursor.fetchall()
    cursor.close()
    return jsonify(exercises)

if __name__ == '__main__':
    app.run(debug=True)
