import web

def listing(**k):
    return web.select('todo', **k)
