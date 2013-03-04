# -*- coding: utf-8 -*-
from django.conf import settings
from jnj import *

def index(request):
    return jrender_to_response('index.html', request=request)
