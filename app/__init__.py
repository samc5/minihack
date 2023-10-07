from flask import Flask, render_template
from flask import session
from flask import request
from flask import redirect
import db_tools
import os
from flask import jsonify
app = Flask(__name__)
app.secret_key = os.urandom(32)

@app.route("/")       
def hello_world():
    """Return base page. Mostly so it doesn't crash"""
    return render_template('math.html')

name_conversion = {"grade1": "Grade 1", "grade2": "Grade 2", "algebra": "Intro to Algebra", "quadratic": "Quadratic Equations"}

@app.route("/register", methods = ["POST", "GET"])
def entrance():
    print(request.form)
    print(session)
    notice = ""
    if ("login" in request.form):
        #print ("Logging in " + request.form["username"])
        if (db_tools.checkLogin( request.form["username"],  request.form["password"], request.form["user"])):
            session["username"] = request.form["username"]
            session["password"] = request.form["password"]
            username = session["username"]
        else: 
            notice = "Wrong Username or Password. Try again"

    if ("register" in request.form):
        if (not db_tools.register( request.form["username"],  request.form["password"], request.form["user"])):
            notice = "Username Taken"
        else:
            notice = "You've been Registered. Now Please Log In."
    if ("username" in session and "password" in session):
        if request.form["user"] == "student":
            return redirect("/student_home")
        else:
            return redirect("/teacher_home")
    return render_template("login_register.html", message = notice)

@app.route('/getScore', methods=['POST'])
def receive_number():
    data = request.get_json()
    received_number = data['number']
    received_string = data['text']
    print(session)
    print(received_number)
    print(received_string)
    db_tools.create_student_tables(db_tools.student_id_from_username(session["username"]),db_tools.find_courseid_from_title(received_string))
    print(db_tools.student_id_from_username(session["username"]))
    print(db_tools.find_courseid_from_title(received_string))
    print(received_string)
    print(received_number)
    db_tools.add_quiz_grade(db_tools.student_id_from_username(session["username"]),db_tools.find_courseid_from_title(received_string), received_string, received_number)
    #create_student_tables
    # You can now work with the received number in Python
    # For this example, we'll just return it
    #x = jsonify({'message': {received_number}})
    #print(x)
    return redirect("/student_home")

@app.route("/student_home", methods = ["POST", "GET"])
def home():
    if ("username" in session and "password" in session):
        username = session["username"]
        courses = db_tools.student_courses(db_tools.student_id_from_username(username))
        titles = []
        for i in courses:
            titles.append(db_tools.get_course_title(i))
        return render_template("student_home.html", usernm = username, courseload=courses, name_conversion = name_conversion, titles=titles)
    else:
        return redirect("/")

@app.route("/teacher_home", methods = ["POST", "GET"])
def teacher_home():
    if ("username" in session and "password" in session):
        username = session["username"]
        t_id = db_tools.teacher_id_from_username(username)
        courses = db_tools.teacher_courses(db_tools.teacher_id_from_username(username))
        print(courses)
        return render_template("teacher_home.html", usernm = username, courseload = courses,id = t_id, lenn = len(courses[0]))
    else:
        return redirect("/")

@app.route("/create_course", methods = ["POST", "GET"])
def create_course():
    if ("username" in session and "password" in session):
        username = session["username"]
        if request.form:
            db_tools.start_course(request.form["class_type"], db_tools.teacher_id_from_username(username))
            return redirect("/teacher_home")
        return redirect("/")
    else:
        return redirect("/")

@app.route("/join_course", methods = ["POST", "GET"])
def join_course():
    if ("username" in session and "password" in session):
        username = session["username"]
        if request.form:
            print("AAAAAAAAAAAAAAAAAAAA")
            db_tools.addStudentToClass(request.form["class_id"], db_tools.student_id_from_username(username))
            return redirect("/student_home")
        return redirect("/")
    else:
        return redirect("/")
if __name__ == "__main__":  # true if this file NOT imported
    app.debug = True        # enable auto-reload upon code change
    app.run()               # launch Flask/////////////