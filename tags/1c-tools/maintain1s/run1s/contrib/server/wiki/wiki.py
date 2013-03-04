#!/usr/bin/python
# Simplistic wiki for localhost, by Adam Bachman
import web, time, os
# mkdirs, read, write, exists, text processing (htmlize), tname 
from utilities import * 

render = web.template.render('templates/')
web.template.Template.globals['htmlize'] = htmlize

urls = ('/favicon.ico$', 'icon',
	'/([a-zA-Z_0-9]*)', 'view',
	'/edit/([a-zA-Z_0-9]*)', 'edit',
	'/links/([a-zA-Z_0-9]*)', 'links',
	'/~info', 'info',
	)

class icon:
    def GET(self):
	pass

class view:
    def GET(self, name):
	if name == '': name = 'index'
	text = read(cur+name)
	if text is None: web.seeother('/edit/'+name)
	print render.view(name, text)

class edit:
    def GET(self, name):
	text = read(cur+name)
	if text is None: text = "edit text here"
	print render.edit(name, text)

    def POST(self, name):
	#if exists(cur+name): write(bak+bakname(name), read(cur+name))
	write(cur+name, web.input().page_text)
	web.seeother('/'+name)


class links:
    def GET(self, name):
	t = read(cur+name)
	b = sorted(Links().backlinks[name])
	f = sorted(allinks(t))
	if b == []: b = ['None']
	if f == []: f = ['None']
	backlist = "* "+"\n* ".join(b); forlist = "* "+"\n* ".join(f)
	text="## Backlinks\n\n"+backlist+"\n\n## Forward Links\n\n"+forlist
	print render.view(name, text)


class info:
    def GET(self):
	L = Links()
	pages = ls(cur)
	text = read('templates/info') % (len(pages),'\n* '.join(L.orphans), 
	', '.join(L.mostfl),L.maxfl,', '.join(L.mostbl),L.maxbl,L.totalinks)
	name = ''
	print render.info(name, text)


if __name__=="__main__":
    web.internalerror = web.debugerror
    web.application(urls).run()
