# -*- coding: utf-8 -*-
'''
application dispatcher.
TODO:
	- add MIDLEWARE
'''
#	settings.INSTALLED_APPS	urls.urlpatterns	index.html
apps = (
	('sro2', (r'^sro2/', 'sro2.urls'), ("{% url sro2.views.index %}", "СРО2")),
	('todo', (r'^todo/', 'todo.urls'), ("{% url todo.views.index %}", "ToDo")),
)
