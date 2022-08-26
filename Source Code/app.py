from flask import Flask, request,jsonify,render_template
from flask.scaffold import setupmethod
from werkzeug.wrappers import response
import model
from quizz_creator import Quiz_Creator




app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")



@app.route("/adduser",methods = ["POST"])
def adduser():
    request_data = request.get_json()
    name = request_data["name"]
    token = request_data["token"]

    
    if token=="7fcfa0fb29": # checking for admin
        response = model.add_user_model(name)
        return jsonify(response)
    else:
        return {"status":400, "errmesg":"Only admin can add users OR invalid admin token"}



@app.route('/deleteuser' , methods = ["DELETE"])
def deleteuser():
    request_data = request.get_json()
    token = request_data["token"]
    user_id = request_data["id"]

    if user_id == token:
        return {"status":403, "errmesg": "Cannot delete admin"}
    if token =="7fcfa0fb29": # checking for admin
        response = model.delete_user_model(user_id)
        return jsonify(response)
    else:
        return "Only Admin can delete user OR Invalid admin token"



@app.route('/addquestion',methods = ["POST"])
def add_question():
    request_data = request.get_json()
    id = request_data["id"]
    question = request_data["question"]
    choice1 = request_data["choice1"]
    choice2 = request_data["choice2"]
    choice3 = request_data["choice3"]
    choice4 = request_data["choice4"]
    key = request_data["key"]
    marks = request_data["marks"]
    remarks = request_data["remarks"]
    token = request_data["token"]
    
    if token =="7fcfa0fb29": #checking for admin
        response = model.add_question_model(id,question,choice1,choice2,choice3,choice4,key,marks,remarks)
        return jsonify(response)

    else:
        return "Only Admin can add questions OR invalid Admin token"


@app.route('/deletequestion',methods = ["DELETE"])
def delete_question():
    request_data = request.get_json()
    id = request_data["id"]
    token = request_data["token"]

    if token =="7fcfa0fb29":
        response = model.delete_question_model(id)
        return jsonify(response)
    else:
        return "Only admin can delete question OR invalid Admin token"


@app.route("/quiz/", methods=["GET","POST"])
def quiz():
    request_data = request.json
    token = request_data["token"]
    quiz_id = request_data["quiz_id"]
    if request.method == "GET":
        
            uid = model.get_user_id_from_token(token)
            response = Quiz_Creator.render(quiz_id,uid)
            return jsonify(response), 200
        
            #return jsonify({"status":"400", "errmsg":"Invalid user token."}), 405
    elif request.method == "POST":
        answerkeys = request_data["answerkeys"]
        #token == "825ef7528b":
        response = model.evaluate_score(answerkeys, quiz_id)        
        return jsonify(response), response["status"]
        #else:
            #return jsonify({"errmesg":"Invalid user token", "status":400}), 400


@app.route("/generatequiz/", methods=["POST"])
def generatequiz():
    request_data = request.get_json()
    token = request_data["token"]
    nquestions = request_data["nquestions"]

    if token == "7fcfa0fb29":
        response = model.generate_quiz(nquestions)
        return jsonify(response)



if __name__ == "__main__":
    app.run(port = 5000)








