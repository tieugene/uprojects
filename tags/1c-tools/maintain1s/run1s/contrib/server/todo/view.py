import web
import db
import config
import datetime

render = web.template.render('templates/', cache=config.cache)

def listing(**k):
    l = db.listing(**k)
    return render.listing(l)

def datestr(x):
    """
    Can't seem to set mysql creation ddl to UTC, so we'll have to adjust the datestr
    function to localtime which we will assume is the same as your database server.
    """
    return web.datestr(x, datetime.datetime.now())

web.template.Template.globals.update(dict(
  datestr = datestr,
  render = render
))
