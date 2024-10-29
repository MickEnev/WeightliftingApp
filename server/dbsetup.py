# this file is supposed to run once.
# Running this file again will just end in errors
# If this file needs to be redone or edited,
# We need to delete the views and procedures this file has already set up in mysql or other dbms

#imports 
import mysql.connector


# connecting to database

# # MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="test_root",
    database="logbook"
)