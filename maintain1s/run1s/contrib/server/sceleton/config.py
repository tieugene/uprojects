import web
#web.config.db_parameters = dict(dbn='postgres', db='appname', user='username', pw='')
web.config.db_parameters = dict(dbn='sqlite', db='appname')
web.webapi.internalerror = web.debugerror
middleware = [web.reloader]
cache = False
