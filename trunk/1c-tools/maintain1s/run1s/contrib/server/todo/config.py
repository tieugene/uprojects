import web, os
# PLEASE CHANGE THE EMAIL ADDRESSES
#for developing:
#export LOCAL=1

web.config.db_parameters = \
dict(dbn='mysql',host="mysql.dabase.com",user="todo",passwd="eeSh0Uz5",db="todo")

def send(fromaddr, toaddrs, msg):
    """Send an email message. """

    import smtplib

    s = smtplib.SMTP()
    s.connect()
    s.sendmail(fromaddr, [toaddrs], msg)
    s.close()

olderror = web.webapi.internalerror

def error():
    # http://surink.com/cx7
    olderror()
    import sys, traceback
    tb = sys.exc_info()
    text = """From: the bugman <bugs@todo.dabase.com>
To: the bugfixer <kai.hendry@gmail.com>
Subject: bug: %s: %s (%s)
Content-Type: multipart/mixed; boundary="----here----"

------here----
Content-Type: text/plain
Content-Disposition: inline

%s

%s

------here----
""" % (tb[0], tb[1], web.ctx.path, web.ctx.method+' '+web.ctx.home+web.ctx.fullpath,
     ''.join(traceback.format_exception(*tb)))

    #text += str(web.debugerror())
    send('bugs@todo.dabase.com', 'kai.hendry@gmail.com', text)

web.webapi.internalerror = error 

if "LOCAL" in os.environ:

    middleware = [web.reloader]
    cache = False

else:
    middleware = []
    cache = True
