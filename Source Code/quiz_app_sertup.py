from model import token_generator
import sqlite3
from sqlite3.dbapi2 import Cursor


connection = sqlite3.connect('Quiz.db')
cursor = connection.cursor()

create_table1 = "CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT ,name VARCHAR(255),token VARCHAR(255) unique)"  
cursor.execute(create_table1)

create_table2 = "CREATE TABLE questions( id INTEGER PRIMARY KEY, question VARCHAR(1000),choice1 VARCHAR(255),choice2 VARCHAR(255),choice3 VARCHAR(255), choice4 VARCHAR(255),key INTEGER,marks INTEGER,remarks VARCHAR(255))"
cursor.execute(create_table2)

create_table3 = "CREATE TABLE quiz( id INTEGER PRIMARY KEY, quizpaper VARCHAR(2000), answerkeys VARCHAR(200))"
cursor.execute(create_table3)

create_table4 = "CREATE TABLE test_instance(id INTEGER PRIMARY KEY, quizid INTEGER REFERENCES quiz(id), userid INTEGER REFERENCES USers(id), answerkey VARCHAR(255), score INTEGER)"
cursor.execute(create_table4)


#token1 = token_generator()
token1=token_generator()
admin = (10000,'Admin',token1)
insert_query1 = "INSERT INTO users VALUES(?,?,?)"
cursor.execute(insert_query1, admin)



connection.commit()
connection.close()


