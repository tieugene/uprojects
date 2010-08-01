import web
import db
import config

render = web.template.render('templates/', cache=config.cache)

def listing(**k):
	l = db.listing(**k)
	return render.listing(l)

web.template.Template.globals.update(dict(
	datestr = web.datestr,
	render = render
))
