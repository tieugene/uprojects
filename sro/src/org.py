# -*- coding: utf-8 -*-

import var

class	list:
	def	GET(self):
		return var.render.org_list(var.root, var.menu)

class	add:
	def	GET(self):
		return var.render.org_view(var.root, var.menu)

class	view:
	def	GET(self, id):
		return var.render.org_view(var.root, var.menu)

class	edit:
	def	GET(self, id):
		return var.render.org_view(var.root, var.menu)

class	delete:
	def	GET(self, id):
		return var.render.org_list(var.root, var.menu)
