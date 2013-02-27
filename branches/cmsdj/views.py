# -*- coding: utf-8 -*-
#from django.views.generic.simple import direct_to_template
from django.conf import settings
#from djangojinja2 import render_to_response
from jnj import *

def index(request):
    #return direct_to_template(request, 'index.html')
    return jrender_to_response('index.html', request=request)
