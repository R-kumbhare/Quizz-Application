import sqlite3
import random
from sqlite3.dbapi2 import Connection, connect 
from quizz_creator import Quiz_Creator


chars = "abcdef0123456789"

def token_generator():
    token = ""
    for x in range (0, 10):
        token_char = random.choice(chars)
        token = token + token_char
    return token



#Adding new user into the database.
def add_user_model(name):
    connection = sqlite3.connect('Quiz.db')
    cursor = connection.cursor()

    token = token_generator()
    
    user = (name ,token)
    insert_query = "INSERT INTO users(name,token)VALUES(?,?)"
    cursor.execute(insert_query, user)
    connection.commit()
    connection.close()
    return {"status":200, "errmsg":"","newuser":"user added successfully"}
    
#Deleting user from the Database    
def delete_user_model(id):
    connection = sqlite3.connect('Quiz.db')
    cursor = connection.cursor()
    try :
      delete_query = "DELETE FROM users WHERE id = ?"
      id = (id,)
      cursor.execute(delete_query,id)
      connection.commit()
      connection.close()
      return " user deleted successfully"
    except Exception:
        connection.rollback()
        connection.close()

        return {"status": 400, "errmesg":"Could not delete user OR invalid user ID "}


    
def add_question_model(id,question,choice1,choice2,choice3,choice4,key,marks,remarks):
    connection = sqlite3.connect('Quiz.db')
    cursor = connection.cursor()

    questions = (id,question,choice1,choice2,choice3,choice4,key,marks,remarks)
    insert_query = "INSERT INTO questions VALUES(?,?,?,?,?,?,?,?,?)"
    cursor.execute(insert_query,questions)

    connection.commit()
    connection.close()

    return "question added successfully"


def delete_question_model(id):
    connection = sqlite3.connect('quiz.db')
    cursor = connection.cursor()
    try :
        delete_query = "DELETE FROM questions WHERE id = ?"
       
        id = (id,)
        cursor.execute(delete_query,id)

        connection.commit()
        connection.close()
        return "question deleted successfully"
    except Exception:
        connection.rollback()
        connection.close()
        return {"status": 400, "errmesg":"Could not delete question OR invalid question ID "}


def generate_quiz(nq):
    quiz = Quiz_Creator(nq)
    conn = sqlite3.connect("Quiz.db")
    curr = conn.cursor()
    keys = []
    question_id = quiz.formulate()
    
    for q in question_id:
        curr.execute("select key from questions where id = ?",(q,))
        keys.append(curr.fetchall()[0])
    
    curr.execute("select max(id) from quiz")
    id = curr.fetchall()[0][0]
    #newid = int(id)
    
    id += 1
    try:
        curr.execute("insert into quiz (id, quizpaper, answerkeys) values(?,?,?)", (id, str(question_id), str(keys)))
        conn.commit()
        conn.close()
        return "Quiz added to table"
    except sqlite3.Error as err:
        print("Error : ", err)
    

def evaluate_score(answerkeys, quiz_id):
    try:
        conn = sqlite3.connect("Quiz.db")
        curr = conn.cursor()
        #get the answer keys from table quiz
        curr.execute("select answerkeys from quiz where id = ?", (quiz_id,))
        keys = curr.fetchall()[0][0]
        keys = list(keys.replace(",","").replace("[","").replace("]","").replace(" ", "").replace("(", "").replace(")",""))
        #Fetch the questions from the quiz
        curr.execute("select quizpaper from quiz where id = ?", (quiz_id,))
        questions = curr.fetchall()[0][0]
        questions = list(questions.replace(",","").replace("[","").replace("]","").replace(" ", "").replace("(", "").replace(")",""))
        #Fetch the marks per question for each quiz
        marks = []
        for q in questions:
            curr.execute("select marks from questions where id = ?", (q,))
            marks.append(curr.fetchall()[0][0])
        #evaluate the submitted keys with the keys from the database
        result = []
        score = 0
        max_score = 0
        if len(answerkeys)<=len(keys):
            for i in range(len(answerkeys)):
                max_score += marks[i]
                if (int(answerkeys[i])==int(keys[i])):
                    result.append(1)
                    score+=marks[i]
                else:
                    result.append(0)
                    score += 0
            conn.close()
            return {"result":result, "score":score, "max_score":max_score, "status":200}
        else :
            conn.close()
            return {"result":"Incorrect Keys", "status":200}
    except sqlite3.Error as err:
        print("Error: ", err)
        conn.close()
        return {"errmesg":err}
        
  
def get_user_token(username):
    conn = sqlite3.connect("quiz.db")
    curr = conn.cursor()
    try:
        curr.execute("select token from users where name = ?", (username,))
        token = curr.fetchall()[0][0]
        conn.close()
        return {"status":200, "token":f"{token}"}
    except sqlite3.Error as err:
        print("Error: ", err)
        conn.close()
        return {"status":200, "errmesg":err}


def get_user_id_from_token(token):
    conn = sqlite3.connect("quiz.db")
    curr = conn.cursor()
    try:
        curr.execute("select uid from users where token = ?", (token,))
        uid = curr.fetchall()[0][0]
        conn.close()
        return int(uid)
    except sqlite3.Error as err:
        print("Err : ", err)
        return None

	
    
def add_questions_from_file():
    conn = sqlite3.connect("quiz.db")
    curr = conn.cursor()
    questions = Quiz_Creator.import_file()
    try:
        id = 1
        for q in questions[1:]:
            curr.execute("insert into questions(id, question, choice1, choice2, choice3, choice4, key, marks, remarks) values(?,?,?,?,?,?,?,?,?)", (id, q[0],q[1],q[2],q[3],q[4],q[5],q[6],""))
            id+=1
        
        conn.commit()
        conn.close()
    except sqlite3.Error as err:
        print("Error: ", err)
        return {"status": 200, "errmsg":err}
	



