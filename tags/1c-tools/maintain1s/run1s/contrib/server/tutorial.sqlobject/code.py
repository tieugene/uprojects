#!/bin/env python
import web
from model import Todo

web.config.debug = False
render = web.template.render('templates/')

urls = (
	'/', 'view',
	'/add', 'add',
)

class	view:
	def	GET(self):
		todos = Todo.select()
		return render.view(todos)
class add:
	def	POST(self):
		i = web.input()
		new = Todo(title=i.title)
		raise web.seeother('/#t'+str(new.id))

web.internalerror = web.debugerror

if __name__ == "__main__":
	web.application(urls, globals()).run()
