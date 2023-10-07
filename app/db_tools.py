
import sqlite3   #enable control of an sqlite database
DB_FILE="mydatabase.db"
#==========================================================

def seed():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()  
    c.execute("create table if not exists logins(username text primary key, password text not null, type text, idnum integer);")
    c.execute("create table if not exists students(name text, idnum integer primary key);")
    c.execute("create table if not exists teachers(name text, idnum integer primary key);")
    c.execute("create table if not exists courses(title text, idnum integer primary key, teacher_id integer);")
    print("Seeding done")
    db.commit()
    db.close()


def clear(): #clears homepage and all story tables but not login table. Useful in testing, not so much in actual websites

	db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
	c = db.cursor()  
	c.execute(f'select name from sqlite_master where type = "table" and name = "homepage"')
	bool = c.fetchone()
	if bool:
		count = storyCount()
		#print(count)
		for i in range(count):
			c.execute(f'drop table if exists table{i}')
		c.execute('drop table if exists homepage')
	db.commit()
	db.close()

def register(username, password, usertype): #adds user/password to logins table

	db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
	c = db.cursor()  	
	usrnm = (username,)
	c.execute('select count(username) from logins where username = ?',usrnm)
	num = c.fetchone()[0]
	if num == 1:
		print("uh that username has already been taken") #tell user the username already exists and do this whole thing again
		db.commit()
		db.close()
		return False
	else:
		#count number of users of the same type
		c.execute(f'select count(username) from logins where type = "{usertype}"')
		num = c.fetchone()[0]
		info = (username,password,usertype,num,)
		c.execute(f'insert into logins values(?, ?,?,?)',info)
		db.commit()
		db.close()
		return True

def checkLogin(username, password, user_type): #checks if password is right

	db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
	c = db.cursor()  
	usrnm = (username,)
	c.execute(f'select password from logins where username = ?',usrnm)
	pw = c.fetchone()
	c.execute(f'select type from logins where username = ?',usrnm)
	usr_type = c.fetchone()
	if(not (pw == None)):
		pw = pw[0]
		if (pw == password and usr_type[0] == user_type):
			db.commit()
			db.close()
			return True
	db.commit()
	db.close()
	return False

def courseCount(): #counts how many stories on homepage

	db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
	c = db.cursor()  

	c.execute('select count(title) from courses;')
	num = c.fetchone()[0]
	db.commit()
	db.close()
	return num

def list_of_pages(): #2D array of tables on homepage

	db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
	c = db.cursor()  

	num = storyCount()
	matrix = [[] for i in range(num)]
	#matrix = [ [' '] * 2 for i in range(num)]
	for i in range(num):
		command = f'select title from homepage where idnum = {i};'
		#print(i)
		#print(command)
		c.execute(command)
		title = str(c.fetchone()[0])
		#print(title)
		matrix[i] = [title,i]
		#matrix.append(c.fetchone()[0])
	db.commit()
	db.close()
	return matrix

def start_course(title, teacher_id):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    count = courseCount()
    print(title, teacher_id)
    c.execute(f'insert into courses(title, idnum, teacher_id) values(?, ?, ?)', (title, count, teacher_id))
    c.execute(f'create table if not exists course_{count}(idnum integer, title text, entrynum integer primary key, teacher_id integer, students text)')
    
    first = (title, teacher_id)
    cmd = f'insert into course_{count} values({count},?, 0, ?, "")'
    c.execute(cmd, first)
    
    db.commit()
    db.close()


def user_check(username, idnum): #checks if username has already edited the story

	db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
	c = db.cursor()  
	cmd = f'select 1 from table{idnum} where username = ?'
	first = (username,)
	c.execute(cmd, first)
	bool = c.fetchone()
	db.commit()
	db.close()
	return bool != None

def teacher_id_from_username(username):
	db = sqlite3.connect(DB_FILE)
	c = db.cursor()
	c.execute(f'select idnum from logins where username = "{username}"')
	idnum = c.fetchone()[0]
	db.commit()
	db.close()
	return idnum
def student_id_from_username(username):
	db = sqlite3.connect(DB_FILE)
	c = db.cursor()
	c.execute(f'select idnum from logins where username = "{username}"')
	idnum = c.fetchone()[0]
	db.commit()
	db.close()
	return idnum

def teacher_courses(teacher_id):
	db = sqlite3.connect(DB_FILE)
	c = db.cursor()
	c.execute(f'select title, idnum from courses where teacher_id = {teacher_id}')
	courses = c.fetchall()
	students = []
	quizGrades = []
	for i in range(len(courses)):
		s = getStudentsFromClass(courses[i][1])
		students.append(s)
		for jj in s:
			quizGrades.append(get_quiz_grades(jj, courses[i][1]))
		
	db.commit()
	db.close()
	return courses, students, quizGrades

def student_courses(student_id): #return a list of course ids where the students string includes the student id
	db = sqlite3.connect(DB_FILE)
	c = db.cursor()
	c.execute(f'select idnum from courses')
	courses = c.fetchall()
	student_courses = []
	for i in range(len(courses)):
		students = getStudentsFromClass(courses[i][0])
		if str(student_id) in students:
			student_courses.append(courses[i][0])
	db.commit()
	db.close()
	return student_courses

def get_course_title(course_id):
	db = sqlite3.connect(DB_FILE)
	c = db.cursor()
	c.execute(f'select title from courses where idnum = {course_id}')
	title = c.fetchone()[0]
	db.commit()
	db.close()
	return title

def getStudentsFromClass(courseid):
	db = sqlite3.connect(DB_FILE)
	c = db.cursor()
	c.execute(f'select students from course_{courseid} where idnum = {courseid}')
	students = c.fetchone()[0]

	db.commit()
	db.close()
	return students.split(",")

def addStudentToClass(idnum, student_id): #adds student to class

    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()  
    c.execute(f'select students from course_{idnum} where idnum = {idnum}')
    students = c.fetchone()[0]
    if (students == ""):
        students = str(student_id)
    else:
        students = students + "," + str(student_id)
    c.execute(f'update course_{idnum} set students = ? where idnum = {idnum}', (students,))
    db.commit()
    db.close()

def create_student_tables(student_id, course_id): #creates a table if not exists of a student's grades on each quiz in a course
    
        db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
        c = db.cursor()  
        c.execute(f'create table if not exists student_{student_id}_course_{course_id}(course_id integer, quiz text, score integer)')
        db.commit()
        db.close()

def add_quiz_grade(student_id, course_id, quiz, score): #adds a quiz grade to a student's table, creates the quiz entry if it doesn't exist
        
            db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
            c = db.cursor()  
            c.execute(f'select 1 from student_{student_id}_course_{course_id} where quiz = ?', (quiz,))
            bool = c.fetchone()
            if (bool == None):
                c.execute(f'insert into student_{student_id}_course_{course_id} values({course_id}, ?, ?)', (quiz, score))
            else:
                c.execute(f'update student_{student_id}_course_{course_id} set score = ? where quiz = ?', (score, quiz))
            db.commit()
            db.close()

def find_courseid_from_title(title):
	db = sqlite3.connect(DB_FILE)
	c = db.cursor()
	c.execute(f'select idnum from courses where title = "{title}"')
	idnum = c.fetchone()[0]
	db.commit()
	db.close()
	return idnum


def get_quiz_grades(student_id, course_id): #returns a list of tuples of the form (quiz, score) for a student in a course, only if it exists
	db = sqlite3.connect(DB_FILE)
	c = db.cursor()
	# fetch it only if it exists
	table_name = f'student_{student_id}_course_{course_id}'
	c.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
	table_exists = c.fetchone() is not None
	if table_exists:
		# The table exists, so you can now execute your SELECT query
		c.execute(f'select quiz, score from student_{student_id}_course_{course_id}')
		grades = c.fetchall()
		db.commit()
		db.close()
		return grades  # Fetch and process the result here
	else:
		return []


def print_every_table(): #prints every table in the database
        db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
        c = db.cursor()  
        c.execute("select name from sqlite_master where type = 'table'")
        print(c.fetchall())
        for i in range(courseCount()):
                c.execute(f'select * from course_{i}')
                print(c.fetchall())
       #print student 2s quiz grades in course 0
        c.execute('select * from student_6_course_0')
        print(c.fetchall())
        db.commit()
        db.close()

def print_logins(): #prints every table in the database
		db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
		c = db.cursor()  
		c.execute("select * from logins")
		print(c.fetchall())
		db.commit()
		db.close()

def clear_logins(): #clears logins table
		db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
		c = db.cursor()  
		c.execute("drop table if exists logins")
		c.execute("create table if not exists logins(username text primary key, password text not null, type text, idnum integer);")
		db.commit()
		db.close()
def clear_courses():
	db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
	c = db.cursor()  
	c.execute("drop table if exists courses")
	c.execute("create table if not exists courses(title text, idnum integer primary key, teacher_id integer);")
	db.commit()
	db.close()
def clear_specific_course():
	db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
	c = db.cursor()
	for i in range(1000):
		c.execute(f'drop table if exists course_{i}')
	db.commit()
	db.close()

# #==========================================================
#clear()
seed()
#print(getStudentsFromClass(0))
#print(student_courses(4))
#register("testUsername","whondurfulpassword")	
#print(checkLogin("testUsername","whondurfulpassword"))
#print(checkLogin("testUsername","notwhondurfulpassword"))
#start_story("Sammy the Seal", "is it you, Agnes?", "sydHoff")
#print(user_check("sydHoff",0))
#addToStory(0,"No, Mrs. Jackson.","sydHoff (parody)")
#addToStory(0,"Well then who could be barking like a seal?","sydHoff (real)")
#start_story("Sammy the Squirrel", "Sammy the Squirrel?", "sydHoff")
#addToStory(0,"No, Mrs. Jackson.","sydHoff (parody)")
#addToStory(1,"No, Mrs. Jackson.","sydHoff (preal)")
#addToStory(1,"Sammy is on vacation in Bermuda.","sydHoff (parrot)")
#addToStory(1,"Said Agnes.","sydHoff (parody)")
#start_course("Math", 1)
#clear_logins()
#addStudentToClass(0, 2)
#create_student_tables(2, 0)
#add_quiz_grade(2, 0, "test", 100)
add_quiz_grade(student_id_from_username("6"),find_courseid_from_title("grade1"), "grade1", 0.2)
print(get_quiz_grades(6,0))
print(get_quiz_grades(6,2))
print(find_courseid_from_title("grade1"))
print_every_table()
print_logins()
#clear_courses()
#clear_specific_course()
#print(list_of_pages())
#print(story(0))
#print(prevEntry(0))
#print(story(1))
#print(prevEntry(1))
# #==========================================================


