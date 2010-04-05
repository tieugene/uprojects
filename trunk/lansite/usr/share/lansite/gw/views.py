# -*- coding: utf-8 -*-
'''
GW.views
'''

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import loader, Context, RequestContext
from django.utils.encoding import StrAndUnicode, force_unicode, smart_unicode, smart_str
# 2. other python
from datetime import datetime
# 3. my
from models import *
from forms import *

def	__log_it(request, object, action, change_message=''):
	'''
	Log this activity
	'''
	LogEntry.objects.log_action(
		user_id         = request.user.id,
		content_type_id = ContentType.objects.get_for_model(object).pk,
		object_id       = object.pk, 
		object_repr     = object.asstr(), # Message you want to show in admin action list
		change_message  = u'GW.UI: ' + change_message, # I used same
		action_flag     = action	# django.contrib.admin.models: ADDITION/CHANGE/DELETION
	)


@login_required
def	index(request):
	return render_to_response('gw/index.html')
	if not request.user.is_authenticated():
		return HttpResponseRedirect('../login/?next=%s' % request.path)
		#return HttpResponseRedirect(reverse('lansite.login') + '?next=%s' % request.path)
		#return HttpResponseRedirect(reverse('lansite.login') + '?next=%s' % request.path)
	return render_to_response('gw/index.html')

def	task_list(request):
	return render_to_response('gw/task/task_list.html', context_instance=RequestContext(request, {'item_list': Task.objects.all()}))

def	task_add(request):
	pass

def	task_view(request, item_id):
	# user_type = ContentType.objects.get_for_model(User)
	cid = Task.objects.get(pk=item_id).getclassid()
	if (cid == 1):
		v = 'lansite.gw.views.todo_view'
	if (cid == 2):
		v = 'lansite.gw.views.assign_view'
	return HttpResponseRedirect(reverse(v, kwargs = {'item_id': item_id}))

def	task_edit(request, item_id):
	pass

def	task_del(request, item_id):
	pass

def	task_done(request, item_id):
	pass

def	todocat_add(request):
	if request.method == 'POST':
		form = ToDoCatForm(request.POST)
		if form.is_valid():
			item = form.save(commit=False)
			item.author = GwUser.objects.get(pk=request.user.id)
			item.save()
			return HttpResponseRedirect(reverse('lansite.gw.views.todo_list'))
	else:	# GET
		form = ToDoCatForm()
	return render_to_response('gw/task/todocat_edit.html', context_instance=RequestContext(request, {'form': form}))

def	todocat_view(request, item_id):
	return render_to_response('gw/task/todocat_view.html', context_instance=RequestContext(request, {'item': ToDoCat.objects.get(pk=item_id)}))

def	todocat_edit(request, item_id):
	item = ToDoCat.objects.get(pk=item_id)
	if request.method == 'POST':
		form = ToDoCatForm(request.POST, instance=item)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('lansite.gw.views.todo_list'))
	else:	# GET
		form = ToDoCatForm(instance=item)
	return render_to_response('gw/task/todocat_edit.html', context_instance=RequestContext(request, {'form': form, 'mode': 'Редактирование'}))

def	todocat_del(request, item_id):
	ToDoCat.objects.get(pk=item_id).delete()
	return HttpResponseRedirect(reverse('lansite.gw.views.todo_list'))

def	todocat_add_todo(request, item_id):
	cat = ToDoCat.objects.get(pk=item_id)
	if request.method == 'POST':
		form = ToDoOfCatForm(request.POST)
		if form.is_valid():
			item = form.save(commit=False)
			item.author = GwUser.objects.get(pk=request.user.id)
			item.category = cat
			item.save()
			return HttpResponseRedirect(reverse('lansite.gw.views.todocat_view', kwargs = {'item_id': cat.id}))
	else:	# GET
		form = ToDoOfCatForm()
	return render_to_response('gw/task/todo_edit.html', context_instance=RequestContext(request, {'form': form}))

def	todo_list(request):
	author = GwUser.objects.get(pk=request.user.id)
	return render_to_response('gw/task/todo_list.html', context_instance=RequestContext(request, {'item_list': ToDo.objects.filter(author=author), 'cat_list': ToDoCat.objects.filter(author=author)}))

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

def	todo_done(request, item_id):
	item = ToDo.objects.get(pk=item_id)
	item.done = True
	item.save()
	return HttpResponseRedirect(reverse('lansite.gw.views.todo_list'))


def	assigncat_add(request):
	if request.method == 'POST':
		form = AssignCatForm(request.POST)
		if form.is_valid():
			item = form.save()
			return HttpResponseRedirect(reverse('lansite.gw.views.assign_list'))
	else:	# GET
		form = AssignCatForm()
	return render_to_response('gw/task/assigncat_edit.html', context_instance=RequestContext(request, {'form': form}))

def	assigncat_view(request, item_id):
	return render_to_response('gw/task/assigncat_view.html', context_instance=RequestContext(request, {'item': AssignCat.objects.get(pk=item_id)}))

def	assigncat_edit(request, item_id):
	item = AssignCat.objects.get(pk=item_id)
	if request.method == 'POST':
		form = AssignCatForm(request.POST, instance=item)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('lansite.gw.views.assign_list'))
	else:	# GET
		form = AssignCatForm(instance=item)
	return render_to_response('gw/task/assigncat_edit.html', context_instance=RequestContext(request, {'form': form, 'mode': 'Редактирование'}))

def	assigncat_del(request, item_id):
	AssignCat.objects.get(pk=item_id).delete()
	return HttpResponseRedirect(reverse('gw.views.assign_list'))

def	assign_list(request):
	author = GwUser.objects.get(pk=request.user.id)
	return render_to_response('gw/task/assign_list.html', context_instance=RequestContext(request, {'cat_list': AssignCat.objects.all(), 'item_list': Assign.objects.filter(Q(author=author) | Q(assignee=author))}))

def	assign_add(request):
	'''
	Create action
	'''
	if request.method == 'POST':
		form = AssignForm(request.POST)
		if form.is_valid():
			item = form.save(commit=False)
			item.author = GwUser.objects.get(pk=request.user.id)
			item.created = datetime.now()
			item.save()
			__log_it(request, item, ADDITION)
			return HttpResponseRedirect(reverse('lansite.gw.views.assign_list'))
	else:	# GET
		form = AssignForm()
	return render_to_response('gw/task/assign_edit.html', context_instance=RequestContext(request, {'form': form}))

def	assign_view(request, item_id):
	'''
	Main dispatcher.
	Actions:
		* New: assignee:Accept
		* Accepted: assignee:Route; MkDep; Invalid; Duplicate; Done
		* Completed: author:Approve; author:ReOpen
		* Approved: author:ReOpen
	'''
	return render_to_response('gw/task/assign_view.html', context_instance=RequestContext(request, {
		'item': Assign.objects.get(pk=item_id),
		'form1': UserListForm(),
		'form2': LineCommentForm(),
		'form3': AssignDupForm(),
	}))

def	assign_edit(request, item_id):
	item = Assign.objects.get(pk=item_id)
	if request.method == 'POST':
		form = AssignForm(request.POST, instance=item)
		if form.is_valid():
			item = form.save()
			return HttpResponseRedirect(reverse('lansite.gw.views.assign_list'))
	else:	# GET
		form = AssignForm(instance=item)
	return render_to_response('gw/task/assign_edit.html', context_instance=RequestContext(request, {'form': form}))

def	assign_del(request, item_id):
	item = Assign.objects.get(pk=item_id)
	__log_it(request, item, DELETION)
	item.delete()
	return HttpResponseRedirect(reverse('gw.views.assign_list'))

def	assign_route(request, item_id):
	'''
	Route action: set assignee to new; set state to new;
	'''
	item = Assign.objects.get(pk=item_id)
	if request.method == 'POST':
		if request.POST['user']:
			uid = int(request.POST['user'])
			if (uid != request.user.id):
				item.assignee = GwUser.objects.get(pk=uid)
				item.read = False
				item.save()
				__log_it(request, item, CHANGE, u'Routed to %s' % item.assignee)
				return HttpResponseRedirect(reverse('lansite.gw.views.assign_list'))
	return assign_view(request, item_id)

def	assign_invalid(request, item_id):
	'''
	Invalid action: set state to done, w/ comments
	'''
	# FIXME:
	#__log_it(request, item, CHANGE, u'Invalid: %s' % item.assignee)
	return assign_done(request, item_id)

def	assign_duped(request, item_id):
	'''
	Duplicate action set state to done, w/ comments
	'''
	# FIXME:
	#__log_it(request, item, CHANGE, u'Duplicated: %s' % item.assignee)
	return assign_done(request, item_id)

def	assign_accept(request, item_id):
	'''
	Accept action: set state to done
	'''
	item = Assign.objects.get(pk=item_id)
	item.read = True
	item.save()
	__log_it(request, item, CHANGE, u'Accepted')
	return HttpResponseRedirect(reverse('lansite.gw.views.assign_view', kwargs={'item_id': item.id}))

def	assign_done(request, item_id):
	'''
	Done action
	'''
	item = Assign.objects.get(pk=item_id)
	item.done = True
	item.read = False
	item.save()
	__log_it(request, item, CHANGE, u'Done')
	return HttpResponseRedirect(reverse('lansite.gw.views.assign_view', kwargs={'item_id': item.id}))

def	assign_approve(request, item_id):
	'''
	Approve action
	'''
	__log_it(request, item, CHANGE, u'Approved')
	return assign_accept(request, item_id)

def	assign_reopen(request, item_id):
	'''
	ReOpen action
	'''
	item = Assign.objects.get(pk=item_id)
	item.done = False
	item.read = False
	item.save()
	__log_it(request, item, CHANGE, u'Reopened')
	return HttpResponseRedirect(reverse('lansite.gw.views.assign_view', kwargs={'item_id': item.id}))

def	assign_mkdep(request, item_id):
	'''
	MkDep action
	'''
	return render_to_response('gw/task/assign_view.html')

def	assign_history(request, item_id):
	'''
	History
	'''
	return render_to_response('gw/task/assign_view.html')
