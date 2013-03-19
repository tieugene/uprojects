# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import redirect   #, render_to_response
from django.views.decorators.csrf import csrf_exempt
#from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, update_object, delete_object

from jnj import *
from utils.pager import page_queryset, PAGE_SIZE
import models, forms

# Person CRUD
def person_list(request):
    return jrender_to_response('core/person_list.html', {
        'object_list': page_queryset(models.Person.objects.all(), request.GET.get('page', 1)),
    }, request=request)

def person_detail(request, id):
    return jrender_to_response('core/base.html', {
        'object': models.Person.objects.get(pk=int(id)),
    }, request=request)

# Person
def person_delete(request, id):
    models.Person.objects.get(pk=int(id)).delete()
    return redirect('person_list')

def person_create(request):
	return  create_object (request, model = models.Person, extra_context = {'cancelurl': reverse('person_list')})

def person_update(request, id):
	return  update_object (request, model = models.Person, object_id = id, extra_context = {'cancelurl': reverse('person_detail', args=[id,])})

# PersonAddress
@csrf_exempt
def person_create_address(request, id):
    return __person_sub_create(request, id, forms.PersonAddressForm, 'Новый адрес')

@csrf_exempt
def person_update_address(request, id):
    return __person_sub_update(request, id, models.PersonAddress)

def person_delete_address(request, id):
    return __person_sub_delete(request, id, models.PersonAddress)

# PersonPhone
@csrf_exempt
def person_create_phone(request, id):
    return __person_sub_create(request, id, forms.PersonPhoneForm, 'Новый телефон')

@csrf_exempt
def person_update_phone(request, id):
    return __person_sub_update(request, id, models.PersonPhone)

def person_delete_phone(request, id):
    return __person_sub_delete(request, id, models.PersonPhone)

# PersonEmail
@csrf_exempt
def person_create_email(request, id):
    return __person_sub_create(request, id, forms.PersonEmailForm, 'Новый Email')

@csrf_exempt
def person_update_email(request, id):
    return __person_sub_update(request, id, models.PersonEmail)

def person_delete_email(request, id):
    return __person_sub_delete(request, id, models.PersonEmail)

# PersonDocument
@csrf_exempt
def person_create_document(request, id):
    return __person_sub_create(request, id, forms.PersonDocumentForm, 'Новый документ')

@csrf_exempt
def person_update_document(request, id):
    return __person_sub_update(request, id, models.PersonDocument)

def person_delete_document(request, id):
    return __person_sub_delete(request, id, models.PersonDocument)

# PersonCode
@csrf_exempt
def person_create_code(request, id):
    return __person_sub_create(request, id, forms.PersonCodeForm, 'Новый код')

@csrf_exempt
def person_update_code(request, id):
    return __person_sub_update(request, id, models.PersonCode)

def person_delete_code(request, id):
    return __person_sub_delete(request, id, models.PersonCode)

# Person*
def __person_sub_create(request, id, formclass, title):
    #return create_object (request, form_class = forms.PersonAddressForm, extra_context = {'cancelurl': reverse('person_detail', args=[id,])})
    person = models.Person.objects.get(pk=int(id))
    if request.method == 'POST':
        form = formclass(request.POST)
        if form.is_valid():
            form.save()
            return redirect('person_detail', id=person.pk)
    else:
        form=formclass(initial = {'person': person})
    return render_to_response(
        'core/person_sub_form.html',
        {
            'form':form,
            'title': '%s %s' % (title, str(person)),
            'cancelurl': reverse('person_detail', args=[id,]),
        }
    )

def __person_sub_update(request, id, subclass):
    person = subclass.objects.get(pk=int(id)).person
    return  update_object (
        request,
        model = subclass,
        object_id = id,
        template_name = 'core/person_sub_form.html',
        post_save_redirect = reverse('person_detail', args=[person.pk,]),
        extra_context = {'cancelurl': reverse('person_detail', args=[person.pk,])}
    )

def __person_sub_delete(request, id, subclass):
    object = subclass.objects.get(pk=int(id))
    person = object.person
    object.delete()
    return redirect('person_detail', id=person.pk)
