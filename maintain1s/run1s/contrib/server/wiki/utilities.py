import os, web, time

cur = 'current/'; bak = 'backup/'

## file based read / write
read = lambda n: exists(n) and file(n, 'r').read() or None
write = lambda n, t: file(n, 'w').write(t)

## General Utilities

exists = os.path.exists
ls = os.listdir
# return filename for backup
bakname = lambda n: n+'.'+time.strftime('%Y%m%d%H%M%S',time.gmtime())

def subber(regex,func): 
    """ simplify regex.sub operations that take a function as first input """
    return lambda t: regex.sub(func,t)

def funclist(funcs, t):
    """ perform in order each function in funcs on t """
    for f in funcs: t = f(t)
    return t

## Plugins ##

class TextProc:
    """ Simple text processor.  Take plaintext, return HTML or info. """
    cc = web.re_compile('(?<!\\\)([A-Z][a-z]*[A-Z]+[a-z]+[a-zA-Z0-9]*)')
    ezlink = web.re_compile('(?<!\\\)\[\[([a-zA-Z_0-9 .]+)\]\]')
    include = web.re_compile('(?<!\\\)\{{([a-zA-Z_0-9 ]+)}}')
    
    def __init__(self, cc=True,ez=True,inc=True):
	self.ccon = cc
	self.ezon = ez
	self.incon = inc
	self._ccsub = subber(self.cc, self._ccsub)
	self._ezsub = subber(self.ezlink, self._ezsub)
	self._incsub = subber(self.include, self._incsub)
	self.ccf = self.cc.findall
	self.ezf = self.ezlink.findall
    
    def allinks(self, t):
	return set(self.ccf(t)+self.ezf(t))
    
    def htmlize(self, t):
	t = self._incsub(t)
	t = self._ccsub(self._ezsub(t))
	return str(web.safemarkdown(t))

    # All _...sub(self, mob) methods are meant to run as assisting functions to 
    # regular expression .sub() operations so they take regex match objects as
    # their first argument.
    def _ccsub(self, mob):
	""" replace CamelCase words with links.  This would probably be the
	    first subber you'd want to turn off because it screws with almost 
	    everything else. """
	n = mob.group()
	if not self.ccon: return n
	if exists(cur+n):
	    return '[%s](/%s)'%(n,n) 
	else: 
	    return '%s[?](/edit/%s)'%(n,n)
    
    def _ezsub(self, mob):
	""" replace ezlinks, ignore CamelCase ezlinks. 
	    always ezsub before cc """
	n = mob.groups()[0].replace('_',' ')
	_n = n.replace(' ','_')
	if not self.ezon: return n        
	if self.cc.match(n): 
	    return n
	elif exists(cur+_n): 
	    return '[%s](/%s)'%(n,_n)
	else: 
	    return '%s[?](/edit/%s)'%(n,_n)
	
    def _incsub(self, mob):
	""" replace include directives with the text of 
	    the associated page """
	n = mob.groups()[0].replace('_',' ')
	_n = n.replace(' ','_')
	if not self.incon: return n
	return str(read(cur+_n)) + '\n\n*included from* \[[%s]]' % n
    
# cc=True, ez=True, inc=True.  To shut off CamelCase links, set cc to False.
tproc = TextProc()
htmlize = tproc.htmlize
allinks = tproc.allinks

# return a list of all keys whose values' return value is equal to val
forvaleq = lambda d, func, val: [k for k in d if func(d[k]) == val]

## Link information for the wiki.
class Links:
    """ gather link related information """
    f = lambda : file(spc+'.backlinks', 'w')
    
    def __init__(self):
	self._getLinkInformation(dict((n,read(cur+n)) for n in ls(cur) \
	    if not n[0]=='.'))

    def _getLinkInformation(self, p_d):
	""" Get a whole bunch of info on your wiki. """
	self.forlinks = dict((k,allinks(p_d[k])) for k in p_d)
	self.backlinks = dict((k, set()) for k in p_d)
	for page, links in self.forlinks.iteritems():
	    for name in links:
		try:
		    self.backlinks[name].add(page)
		except KeyError:
		    self.backlinks[name] = set((page,))
	self.fl = self.forlinks; self.bl = self.backlinks
	self.flquants = map(len, self.fl.itervalues())
	self.blquants = map(len, self.bl.itervalues())
	self.orphans = forvaleq(self.bl, len, 0)
	self.maxfl = max(self.flquants)
	self.maxbl = max(self.blquants)
	self.mostfl = forvaleq(self.fl, len, self.maxfl)
	self.mostbl = forvaleq(self.bl, len, self.maxbl)
	self.totalinks=sum(self.flquants)+sum(self.blquants)
    
    def update(self, page):
	""" Update backlinks if you've got a persistent 
	    backlink dictionary floating around.  """
	t = read(page)
	current = allinks(t)
	lost = self.links_from[page] - current
	gained = current - self.links_from[page]
	for n in lost: self.backlinks[n].remove(page)
	for n in gained: self.backlinks[n].add(page)
	
# if __name__=="__main__":
