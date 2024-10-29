import mysql.connector

# MySQL connection
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="test_root",
    database="logbook"
)
query = "SET GLOBAL max_allowed_packet=104857600"
mydb.reconnect()
mycursor = mydb.cursor()
mycursor.execute(query)
mycursor.close()

def get_exercise_details(exercise_name):
    mydb.reconnect()
    cursor = mydb.cursor()
    query = f"""
        SELECT ExerciseID, Name, Body_Part, Equipment 
        FROM Exercises 
        WHERE Name LIKE %s
    """
    cursor.execute(query, (f"%{exercise_name}%",))
    result = cursor.fetchone()
    cursor.close()
    return result if result else ['', '', '', '']

def update_exercise_details(id, name, body_part, equipment):
    mydb.reconnect()
    cursor = mydb.cursor()

    curr_details = get_exercise_details(name)
    id = id if id else curr_details[0]
    name = name if name else curr_details[1]
    body_part = body_part if body_part else curr_details[2]
    equipment = equipment if equipment else curr_details[3]

    query = """
        UPDATE Exercises 
        SET Name = %s, Body_Part = %s, Equipment = %s 
        WHERE ExerciseID = %s
    """
    cursor.execute(query, (name, body_part, equipment, id))
    mydb.commit()
    cursor.close()

def add_new_exercise(name, body_part, equipment):
    mydb.reconnect()
    cursor = mydb.cursor()
    query = """
        INSERT INTO Exercises (Name, Body_Part, Equipment) 
        VALUES (%s, %s, %s)
    """
    cursor.execute(query, (name, body_part, equipment))
    mydb.commit()
    cursor.close()
