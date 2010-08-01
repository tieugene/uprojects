from sqlobject import *
import datetime

# change the location at the end for your own purposes
sqlhub.processConnection = connectionForURI("sqlite:///mnt/shares/home/eugene/Projects/uprojects/run1c/web.py/contrib/tutorial.sqlobject/todo.db")
# sqlite3 todo.db 'CREATE TABLE todo (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, created DATETIME DEFAULT CURRENT_TIMESTAMP, done BOOLEAN DEFAULT 'f');'
# sqlite3 todo.db 'INSERT INTO todo (title) VALUES ("Learn web.py");'

class Todo(SQLObject):
	title=StringCol()
	created=DateTimeCol(default=datetime.datetime.now)
	done=BoolCol(default=False)
