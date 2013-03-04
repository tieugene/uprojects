# auth.py: an authentication module for web.py 
# by Jon Rosebaugh 
# You may use this module under whatever license you are using web.py 
# (This is intended to handle the situation if web.py changes licenses) 

import web 
import hmac 
from time import time 

configs = web.storage() 

def setup(args): # this is a problem with web.reloader 
	for k, v in args.iteritems(): 
		configs[k] = v 

def logout(): 
	web.setcookie(configs.cookiename, "", -1, configs.cookiedomain) 

def authpage(theclass, myusertype, myvalidatefunc = None): 
	class newclass(theclass): 
		usertype = myusertype 
		if myvalidatefunc is not None: 
			validatefunc = staticmethod(myvalidatefunc) 
		elif configs.validatefunc is not None: 
			validatefunc = staticmethod(configs.validatefunc) 
		else: 
			raise NotImplementedError, "Must have a validating function" 

		def GET(self, *a, **k): 
			currenturl = web.context.home + web.context.fullpath 
			allcookies = web.cookies() 
			if not allcookies.has_key(configs.cookiename): 
				configs.login(self.usertype, currenturl) 
				return 
			mycookie = allcookies[configs.cookiename] 
			cookielist = mycookie.split('|') 
			theuser = cookielist[1] 
			h = hmac.new(configs.cookiesecret) 
			h.update(cookielist[1]) 
			h.update(cookielist[2]) 
			if not h.hexdigest() == cookielist[0]: 
				configs.invalidlogin(self.usertype, currenturl) 
				return 
			elif (int(time())) > int(cookielist[2]): 
				configs.timeoutlogin(self.usertype, currenturl) 
				return 
			elif not self.validatefunc(self.usertype, theuser): 
				configs.noaccess(self.usertype, currenturl) 
				return 

			# We should be fine, then. 

			if hasattr(theclass, 'GET'): 
				return theclass.GET(self, *a, **k) 

		def POST(self, *a, **k): 
			i = web.input() 

			if i.has_key('username') and i.has_key('password') and i.has_key('auth') and i.auth=='login': 
				username = i.username 
				password = i.password 
				if configs.checkpw(username, password): 
					thetime = str(int(time()+configs.cookietimeout)) 
					h = hmac.new(configs.cookiesecret) 
					h.update(username) 
					h.update(thetime) 
					l = [h.hexdigest(), username, thetime] 
					cookiestring = "|".join(l) 
					web.setcookie(name='auth', value=cookiestring, expires=configs.cookietimeout, domain=configs.cookiedomain) 
					web.seeother(web.context.path) 
				else: 
					currenturl = web.context.home + web.context.fullpath 
					configs.invalidlogin(self.usertype, currenturl) 
					return 

			if hasattr(theclass, 'POST'): 
				return theclass.POST(self, *a, **k) 

	return newclass
