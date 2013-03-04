from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, Context, RequestContext
from django.conf import settings
from jinja2 import FileSystemLoader, Environment, PackageLoader, ChoiceLoader, environmentfilter

from django.utils.datetime_safe import datetime

loader_array = []
for pth in getattr(settings, 'TEMPLATE_DIRS', ()):
    loader_array.append(FileSystemLoader(pth))

for app in settings.INSTALLED_APPS:
    loader_array.append(PackageLoader(app))

default_mimetype = getattr(settings, 'DEFAULT_CONTENT_TYPE')
global_exts = getattr(settings, 'JINJA_EXTS', ())
env = Environment(extensions=global_exts, loader=ChoiceLoader(loader_array))

from django.core import urlresolvers

def url_for(viewname,*args,**kwargs):
   return urlresolvers.reverse(viewname, args=args, kwargs=kwargs)

env.globals['url_for'] =url_for
env.globals['MEDIA_URL'] = settings.MEDIA_URL
env.globals['STATIC_URL'] = settings.STATIC_URL

def datetimeformat(value, format='%d.%m.%Y'):
    try:
        if format == 'd.m.Y':
            format='%d.%m.%Y'
        return value.strftime(format)
    except:
        return value

def datetimenow(format='%d.%m.%Y'):
    d=datetime.now()
    try:
        return d.strftime(format)
    except:
        return 'now'

env.filters['date'] = datetimeformat
env.globals['now'] = datetimenow

def jrender_to_string(filename, context={}):
    template = env.get_template(filename)
    rendered = template.render(**context)
    return rendered

def jrender_to_response(filename, context={}, request=None, mimetype=default_mimetype):
    if request:
        context['request'] = request
        try:
            context['user'] = request['user']
        except:
            context['user'] = request.user
    rendered = jrender_to_string(filename, context)
    return HttpResponse(rendered,mimetype=mimetype)
#'''


def render_to(template):
    def renderer(func):
        def wrapper(request, *args, **kw):
            output = func(request, *args, **kw)
            if isinstance(output, (list, tuple)):
                return jrender_to_response(output[1], output[0], RequestContext(request))
            elif isinstance(output, dict):
                return jrender_to_response(template, output, RequestContext(request))
            return output
        return wrapper
    return renderer