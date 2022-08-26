import csv
import random
import sqlite3
from collections import OrderedDict

class Quiz_Creator():

    def __init__(self, nquestions=None, quizid=None, subject=None):
        self.nquestions = nquestions
        self.quizid = quizid
        self.subject = subject

    ## This function returns a randomised list of question ids from the questions database to create the quiz
    def formulate(self):
        count = 0
        question_id = []
        conn = sqlite3.connect("Quiz.db")
        curr = conn.cursor()
        curr.execute("select max(id) from questions")
        max = curr.fetchall()[0][0]

        while(count < self.nquestions):
            id = random.randint(1,max)
            if (id not in question_id):
                question_id.append(id)
                count+=1
            else:
                continue

        return question_id
        

    @classmethod
    def render(self, qid, uid=None, sort=False):
        connection = sqlite3.connect("Quiz.db")
        cursor = connection.cursor()
        cursor.execute("select quizpaper from quiz where id = ?",(qid,))
        questions_id = cursor.fetchall()[0][0]
        questions_id = questions_id.replace(",","").replace("[","").replace("]","").replace(" ", "")
        q_render = OrderedDict()
        questions_id = list(questions_id)
        count = 1
        for id in questions_id:
            cursor.execute("select question, choice1, choice2, choice3, choice4 from questions where id = ?", (id,))
            quizpaper = (cursor.fetchall()[0])
            qno = "q" + str(count)
            question_entry = OrderedDict()
            question_entry = {"question":quizpaper[0], "choice1":quizpaper[1], "choice2":quizpaper[2], "choice3":quizpaper[3], "choice4":quizpaper[4]}
            q_render[qno] = question_entry
            count+=1
        try:
            cursor.execute("insert into test_instance(quizid, userid) values(?,?)", (qid, uid))
            connection.commit()
            connection.close()
        except sqlite3.Error as err:
            print("Err: ", err)
            connection.close()
            return {"err":err}
        return q_render

    
    
    
    
    @classmethod
    def sort_method(by_marks):
        conn = sqlite3.connect("Quiz.db") 
        cur = conn.cursor()
	
        sql_query  = "SELECT * FROM questions  WHERE marks='%s'"%(by_marks)
        res = cur.execute(sql_query)
	
        val = {"info":list(res)}
	
        conn.commit()
	
        conn.close()
	
        return val


        
		


    
    #Imports csv file and pushes data  into quiz table
    #@classmethod
    #def import_file(self):
    def import_file(self):
        questions = []
        with open("config/questions.csv", "r") as f:
            csv_reader = csv.reader(f, delimiter = ",")
            for row in csv_reader:
                questions.append(row)

        return questions
            

