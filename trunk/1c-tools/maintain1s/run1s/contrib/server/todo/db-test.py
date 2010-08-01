import web, config

web.load()

for i in web.select('todo'):
    print i
