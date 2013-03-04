#!/usr/bin/env python2.4
# Simple CRUD webpy.org example
# hendry at iki.fi

import web, config, view
from view import render

urls = (
    '/', 'index',
    '/add', 'add',
    '/delete', 'delete',
    '/update', 'update'
)

class index:
    def GET(self):
        todos = web.select('todo')
        print render.base(view.listing())

class add:
    def POST(self):
        i = web.input()
        if i.title.strip():
            n = web.insert('todo', title=i.title)
            web.seeother('/#t'+str(n))
        else:
            web.seeother('/')

class delete:
    def POST(self):
        i = web.input()
        web.delete('todo', int(i.id))
        web.seeother('/')

class update:
    def POST(self):
        # http://24ways.org/advent/edit-in-place-with-ajax
        i = web.input()
        if i.content.strip():
            web.update('todo', int(i.id), title=i.content)
            print i.content
            web.seeother('/')
        else:
            # is there a better way to get the original title?
            print web.select('todo', where=("id=%d" % int(i.id)))[0].title

def runfcgi_apache(func):
    web.wsgi.runfcgi(func, None)

if __name__ == "__main__": 
    import os
    #if "LOCAL" not in os.environ:
    #    web.wsgi.runwsgi = runfcgi_apache
    web.run(urls, globals(), *config.middleware)
