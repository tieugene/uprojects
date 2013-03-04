#!/usr/bin/python
# Simplistic wiki for localhost, by Adam Bachman
import web, time, os
from markdown import markdown

urls = ('/([a-zA-Z]*)', 'view', '/_([a-zA-Z]*)', 'edit')

class view:
    def GET(self, name):
	name = name or 'index'
	print render.view(name, getpage(name) or "%s doesn't exist"%name)

class edit:
    def GET(self, name):
	print render.edit(name, getpage(name) or "edit text here")

    def POST(self, name):
	if iscur(name): write(BAK+tname(name), getpage(name))
	write(CUR+name, web.input().page_text)
	web.seeother('/'+name)

## os related utilities
CUR = 'current/'; BAK = 'backup/'; TMPL = 'templates/'
exists = os.path.exists
iscur = lambda n: exists(CUR+n)
mkdirs = lambda dl: [os.mkdir(d) for d in dl if not exists(d)]
mkdirs([CUR,BAK,TMPL])

## file based read / write
tname = lambda n: n+'.'+str(int(time.time()))
getpage = lambda n: iscur(n) and file(CUR+n, 'r').read() or None
write = lambda n, t: file(n, 'w').write(t)

## text formatting (links, includes, markdown)
cc = web.re_compile('([A-Z][a-z]*[A-Z]+[a-z]+[a-zA-Z]*)')
inc = web.re_compile('(?<!\\\){{([A-Z][a-z]*[A-Z]+[a-z]+[a-zA-Z]*)}}')
incify = lambda m: str(getpage(m.groups()[0]))+'\n\n- - - - - \n\n'
_linkify = lambda n: iscur(n) and '[%s](/%s)'%(n,n) or '%s[?](/_%s)'%(n,n)
linkify = lambda m: _linkify(m.group())
htmlize = lambda t: str(markdown(cc.sub(linkify,inc.sub(incify, t))))

if not exists('templates/view.html'): # UGLY, included for convenience
    view=('$def with (name, text)\n<html><head><title>$name </title></head><b'
    'ody><h1><a href="/">@</a> <a href="/_$name">$name </a></h1>$:htmlize(te'
    'xt)\n</body></html>')
    edit=('$def with (name, text)\n<html><head><title>$name </title></head><b'
    'ody><a style="cursor:pointer;" onclick="history.back()"><h1>Editing: $na'
    'me </h1></a><form action="" method="post"><textarea name="page_text" row'
    's="25" style="width:100%">$text</textarea><br /><input type="submit" val'
    'ue="Submit" /></form></body></html>')
    write(TMPL+'view.html', view); write(TMPL+'edit.html',edit)

render = web.template.render(TMPL)
web.template.Template.globals['htmlize'] = htmlize

if __name__=="__main__":
    web.internalerror = web.debugerror
    web.application.run(urls, globals(), web.reloader)
