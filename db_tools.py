
import sqlite3   #enable control of an sqlite database
DB_FILE="discobandit"
#==========================================================
def seed(): #Creates login and homepage tables, should be run before anything else (other than clear)

	db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
	c = db.cursor()  
	c.execute("create table if not exists logins(username text primary key, password text not null, type text);")
	c.execute("create table if not exists homepage(title text, idnum integer primary key);")
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

def register(username, password): #adds user/password to logins table

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
		info = (username,password)
		c.execute(f'insert into logins values(?, ?)',info)
		db.commit()
		db.close()
		return True

def checkLogin(username, password): #checks if password is right

	db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
	c = db.cursor()  
	usrnm = (username,)
	c.execute(f'select password from logins where username = ?',usrnm)
	pw = c.fetchone()
	if(not (pw == None)):
		pw = pw[0]
		if (pw == password):
			db.commit()
			db.close()
			return True
	db.commit()
	db.close()
	return False
def storyCount(): #counts how many stories on homepage

	db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
	c = db.cursor()  

	c.execute('select count(title) from homepage;')
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

def start_story(title, text, username): #creates a table for the story, adds it to homepage db, puts in the first entry

	db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
	c = db.cursor()  	
	count = storyCount()
	c.execute(f'create table if not exists table{count}(idnum integer, title text, entrynum integer primary key, entrytext text, username text)')
	first = (title, text, username)
	cmd = f'insert into table{count} values({count},?, 0, ?, ?)'
	c.execute(cmd, first)
	second = (title,)
	cmd2 = f'insert into homepage values(?, {count})'
	c.execute(cmd2, second)
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

def addToStory(idnum, text, username): #adds new entry to story

	db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
	c = db.cursor()  
	if not user_check(username,idnum):
		count = entryCount(idnum)
		title = getTitle(idnum)
		#print(title)
		cmd = f'insert into table{idnum} values({idnum}, ?, {count}, ?, ?)'
		first = (title, text, username)
		c.execute(cmd, first)
	else:
		print("something has gone wrong - you've already edited the story")
	db.commit()
	db.close()

def getTitle(idnum): #returns title of a story

	db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
	c = db.cursor()  
	c.execute(f'select title from homepage where idnum = {idnum}')
	title = str(c.fetchone()[0])
	#print(title)
	db.commit()
	db.close()
	return title

def story(idnum): #returns string of the entire story

	db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
	c = db.cursor()  
	string = ""
	count = entryCount(idnum)
	c.execute(f'select entrytext from table{idnum}')
	for i in c.fetchmany(count):
		string += str(i[0]) + " "
		print(string)
	db.commit()
	db.close()	
	return string
def prevEntry(idnum): #returns string of latest entry

	db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
	c = db.cursor()  
	count = entryCount(idnum)
	c.execute(f'select entrytext from table{idnum} where entrynum = {count - 1}')
	string = c.fetchone()
	if (not string == None):
		string = str(string[0])
	db.commit()
	db.close()
	return string

def entryCount(idnum): #counts entries in a story

	db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
	c = db.cursor()  
	c.execute(f'select entrynum from table{idnum}')
	count = c.fetchall()
	if (count != None):
		count = count[-1][0] 
	db.commit()
	db.close()
	return count + 1



# #==========================================================
#clear()
#seed()
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



#print(list_of_pages())
#print(story(0))
#print(prevEntry(0))
#print(story(1))
#print(prevEntry(1))
# #==========================================================


