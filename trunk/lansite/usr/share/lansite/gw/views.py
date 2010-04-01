# -*- coding: utf-8 -*-
'''
GW.views
'''

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import loader, Context, RequestContext
from django.utils.encoding import StrAndUnicode, force_unicode, smart_unicode, smart_str
# 2. other python
from datetime import datetime
# 3. my
from models import *
from forms import *

def	index(request):
	return render_to_response('gw/index.html')

def	task_list(request):
	return render_to_response('gw/task/task_list.html', context_instance=RequestContext(request, {'item_list': Task.objects.all()}))

def	todocat_list(request):
	return render_to_response('gw/task/todocat_list.html', context_instance=RequestContext(request, {'item_list': ToDoCat.objects.filter(author=GwUser.objects.get(pk=request.user.id))}))

def	todocat_add(request):
	if request.method == 'POST':
		form = ToDoCatForm(request.POST)
		if form.is_valid():
			item = form.save(commit=False)
			item.author = GwUser.objects.get(pk=request.user.id)
			item.save()
			return HttpResponseRedirect(reverse('lansite.gw.views.todocat_list'))
	else:	# GET
		form = ToDoCatForm()
	return render_to_response('gw/task/todocat_edit.html', context_instance=RequestContext(request, {'form': form}))

def	todocat_view(request, item_id):
	return render_to_response('gw/task/todocat_view.html', context_instance=RequestContext(request, {'item': ToDoCat.objects.get(pk=item_id)}))

def	todocat_edit(request, item_id):
	item = ToDo.objects.get(pk=item_id)
	if request.method == 'POST':
		form = ToDoCatForm(request.POST)
		if form.is_valid():
			item = form.save(commit=False)
			return HttpResponseRedirect(reverse('gw.views.todocat_view', kwargs={'item_id': item.id}))
	else:	# GET
		form = ToDoCatForm()
	return render_to_response('gw/task/todocat_edit.html', context_instance=RequestContext(request, {'form': form}))

def	todocat_del(request, item_id):
	return HttpResponseRedirect(reverse('gw.views.todocat_list'))

def	todo_list(request):
	return render_to_response('gw/task/todo_list.html', context_instance=RequestContext(request, {'item_list': ToDo.objects.all()}))

def	todo_add(request):
	if request.method == 'POST':
		form = ToDoForm(request.POST)
		if form.is_valid():
			item = form.save(commit=False)
			item.author = GwUser.objects.get(pk=request.user.id)
			item.created = datetime.now()
			item.save()
			return HttpResponseRedirect(reverse('lansite.gw.views.todo_list'))
	else:	# GET
		form = ToDoForm()
	return render_to_response('gw/task/todo_edit.html', context_instance=RequestContext(request, {'form': form}))

def	todo_view(request, item_id):
	return render_to_response('gw/task/todo_view.html', context_instance=RequestContext(request, {'item': ToDo.objects.get(pk=item_id)}))

def	todo_edit(request, item_id):
	item = ToDo.objects.get(pk=item_id)
	if request.method == 'POST':
		form = ToDoForm(request.POST, instance=item)
		if form.is_valid():
			item = form.save()
			return HttpResponseRedirect(reverse('lansite.gw.views.todo_view', kwargs={'item_id': item.id}))
	else:	# GET
		form = ToDoForm(instance=item)
	return render_to_response('gw/task/todo_edit.html', context_instance=RequestContext(request, {'form': form}))

def	todo_del(request, item_id):
	ToDo.objects.get(pk=item_id).delete()
	return HttpResponseRedirect(reverse('lansite.gw.views.todo_list'))

def	assigncat_list(request):
	return render_to_response('gw/task/todocat_list.html', context_instance=RequestContext(request, {'item_list': TaskCat.objects.all()}))

def	assigncat_add(request):
	return render_to_response('gw/task/todocat_edit.html', context_instance=RequestContext(request, {'item_list': TaskCat.objects.all()}))
	return HttpResponseRedirect(reverse('gw.views.todocat_view', kwargs={'item_id': item.id}))

def	assigncat_view(request, item_id):
	return render_to_response('gw/task/todocat_view.html', context_instance=RequestContext(request, {'item': TaskCat.objects.all()}))

def	assigncat_edit(request, item_id):
	item = ToDo.objects.get(pk=item_id)
	if request.method == 'POST':
		form = ToDoCatForm(request.POST)
		if form.is_valid():
			item = form.save(commit=False)
			return HttpResponseRedirect(reverse('gw.views.todocat_view', kwargs={'item_id': item.id}))
	else:	# GET
		form = ToDoCatForm()
	return render_to_response('gw/task/todocat_edit.html', context_instance=RequestContext(request, {'form': form}))

def	assigncat_del(request, item_id):
	return HttpResponseRedirect(reverse('gw.views.todocat_list'))

def	assign_list(request):
	'''
	Filters:
		* In/Out/All
		* Author (In)
		* Assignee (Out)
		* Category
		* Importance
		* Deadline
		* Done+Read (6)
	Sort:
		* Created
		* Author
		* Assignee
		* Category
		* Importance
		* Deadline
	'''
	return render_to_response('gw/task/assign_list.html', context_instance=RequestContext(request, {'item_list': Assign.objects.all()}))

def	assign_add(request):
	'''
	Create action
	'''
	return render_to_response('gw/task/assign_edit.html')

def	assign_view(request, item_id):
	'''
	Main dispatcher.
	Actions:
		* New: Accept
		* Accepted: Route; MkDep; Invalid; Duplicate; Done
		* Completed: Approve; ReOpen
		* Approved: ReOpen
	'''
	return render_to_response('gw/task/assign_view.html')

def	assign_edit(request, item_id):
	return render_to_response('gw/task/assign_edit.html')

def	assign_del(request, item_id):
	'''
	Create action
	'''
	return render_to_response('gw/task/assign_list.html')

def	assign_route(request, item_id):
	'''
	Route action: set assignee to new; set state to new;
	'''
	return render_to_response('gw/task/assign_view.html')

def	assign_invalid(request, item_id):
	'''
	Invalid action: set state to done, w/ comments
	'''
	return render_to_response('gw/task/assign_view.html')

def	assign_duped(request, item_id):
	'''
	Duplicate action set state to done, w/ comments
	'''
	return render_to_response('gw/task/assign_view.html')

def	assign_accept(request, item_id):
	'''
	Accept action: set state to done
	'''
	return render_to_response('gw/task/assign_view.html')

def	assign_done(request, item_id):
	'''
	Done action
	'''
	return render_to_response('gw/task/assign_view.html')

def	assign_approve(request, item_id):
	'''
	Approve action
	'''
	return render_to_response('gw/task/assign_view.html')

def	assign_reopen(request, item_id):
	'''
	ReOpen action
	'''
	return render_to_response('gw/task/assign_view.html')

def	assign_mkdep(request, item_id):
	'''
	MkDep action
	'''
	return render_to_response('gw/task/assign_view.html')
