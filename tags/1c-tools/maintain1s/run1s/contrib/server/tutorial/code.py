#!/bin/env python
import web

web.config.debug = False
render = web.template.render('templates/')
db = web.database(dbn='sqlite', db='dbname')	# sqlite3 dbname 'CREATE TABLE todo (id serial primary key, title text, created timestamp, done boolean default 'f'); INSERT INTO todo (title) VALUES ("Learn web.py");'

urls = (
	'/', 'index',
	'/add', 'add',
)
app = web.application(urls, globals())

class	index:
	def GET(self):
		todos = db.select('todo')
		return render.index(todos)
class add:
	def POST(self):
		i = web.input()
		n = db.insert('todo', title=i.title)
		raise web.seeother('/')

if __name__ == "__main__":
	app.run()
