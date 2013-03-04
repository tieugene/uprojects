#!/bin/env python
import web
import view, config
from view import render

urls = (
	'/', 'index'
)

class index:
	def GET(self):
		print render.base(view.listing())

if __name__ == "__main__":
	web.run(urls, globals(), *config.middleware)