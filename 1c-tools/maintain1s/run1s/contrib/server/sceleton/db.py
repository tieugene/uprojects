import web

def listing(**k):
	return web.select('items', **k)
