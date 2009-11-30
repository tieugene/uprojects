#!/bin/env python
# -*- coding: utf-8 -*-

import simplejson as json

# 1. load data
data = json.load(open('sro.json', 'r'))
permitown = list()
for i, a in enumerate(data):
	if a['model'] == 'sro.permit':
# 2. create new permitowns
		permitown.append({
			'pk':		a['pk'],
			'model':	'sro.permitown',
			'fields':	{
				'permit':	a['pk'],
				'date':		a['fields']['date'],
				'regno':	a['fields']['regno'],
				'meeting':	a['fields']['meeting']
			}
		})
# 3. tune old permit:
# 3.1. remove unwanted fields
		del data[i]['fields']['date']
		del data[i]['fields']['regno']
		del data[i]['fields']['meeting']
# 3.2. add type
		data[i]['fields']['permittype'] = 1
# 4. add permittype
data.extend([
	{ 'pk': 1, 'model': 'sro.permittype', 'fields': { 'id':	1, 'name': 'Permition' } },
	{ 'pk': 2, 'model': 'sro.permittype', 'fields': { 'id':	2, 'name': 'Statement' } },
	{ 'pk': 3, 'model': 'sro.permittype', 'fields': { 'id':	3, 'name': 'Alien permition' } },
])
# 5. merge data
data.extend(permitown)
# 6. flush
json.dump(data, open('sro_new.json', 'w'), indent=1)
