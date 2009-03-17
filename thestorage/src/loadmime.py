#!/bin/env python
'''
Load mime* from xdg
DB: {
	<media>: {
		<subtype>:
			[comment, [
				ext,
				]
			...]
		},
	...
}
'''

from xdg import Mime
import web, pprint
import config

db = {}

# 0. init Mime db
Mime.get_type('')
# 1. load mimetypes
for i in Mime.types:
	if i[0] not in db:
		db[i[0]] = {}
	if i[1] not in db[i[0]]:
		db[i[0]][i[1]] = (Mime.lookup(i[0] + "/" + i[1]).get_comment(), [])
# 2. load extentions
for i in Mime.exts.keys():
	m = Mime.exts[i]
	db[m.media][m.subtype][1].append(i)
# 3. load mime db
web.config.debug = False
mydb = web.database(dbn='sqlite', db=config.dbfn)
mydb.delete('mimemedia', where="1=1")
#pprint.pprint(db)
medianames = db.keys()
medianames.sort()
for medianame in medianames:
	media = db[medianame]
	media_id = int(mydb.insert('mimemedia', name = medianame))
	subtypenames = media.keys()
	subtypenames.sort()
	for subtypename in subtypenames:
		subtype = media[subtypename]
		subtype_id = int(mydb.insert('mimesubtype', mediaid = media_id, name = subtypename, comments = subtype[0]))
		subtype[1].sort()
		for e in subtype[1]:
			mydb.insert('mimeext', subtypeid = subtype_id, name = e)
