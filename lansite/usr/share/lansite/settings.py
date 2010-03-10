# -*- coding: utf-8 -*-
# Django settings for lansite project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
	('admin', 'ti.eugene@gmail.com'),
	# ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS
'''
DATABASE_ENGINE = 'sqlite3'	# 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = '/mnt/shares/lansite/db/lansite.db'	# Or path to database file if using sqlite3.
DATABASE_USER = ''		# Not used with sqlite3.
DATABASE_PASSWORD = ''		# Not used with sqlite3.
DATABASE_HOST = ''		# Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''		# Set to empty string for default. Not used with sqlite3.
'''
DATABASE_ENGINE = 'mysql'	# 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'lansite'	# Or path to database file if using sqlite3.
DATABASE_USER = 'lansite'		# Not used with sqlite3.
DATABASE_PASSWORD = 'lansite'		# Not used with sqlite3.
DATABASE_HOST = 'localhost'		# Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''		# Set to empty string for default. Not used with sqlite3.

SEND_EMAILS = False       # make it True and edit settings bellow if you want to receive emails
EMAIL_HOST = ''           # smtp.myhost.com
EMAIL_HOST_USER = ''      # user123
EMAIL_HOST_PASSWORD = ''  # qwerty
EMAIL_ADDRESS_FROM = ''   # noreply@myhost.com
if DEBUG:
	EMAIL_FAIL_SILENTLY = False
else:
	EMAIL_FAIL_SILENTLY = True

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL= '/'

import sys, os
PROJECT_DIR = os.path.dirname(__file__)
sys.path.append(PROJECT_DIR)

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Moscow'
DATE_FORMAT = 'd/m/Y'
# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'ru-RU'
DEFAULT_CHARSET = 'utf-8'
SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

FILE_CHARSET = 'utf-8'

SESSION_SAVE_EVERY_REQUEST = False

# Make this unique, and don't share it with anybody.
SECRET_KEY = '#*9#i03#2cy2p&z9bogb0s5sq+(cay6z!5p$8!i&2=mdqddjwa'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
	'django.template.loaders.filesystem.load_template_source',
	'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
	'django.middleware.common.CommonMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.middleware.transaction.TransactionMiddleware',
	'django.middleware.doc.XViewMiddleware',
	'todo.middleware.Custom403Middleware',
)

AUTHENTICATION_BACKENDS = (
	'django.contrib.auth.backends.ModelBackend',
)


ROOT_URLCONF = 'urls'

TEMPLATE_CONTEXT_PROCESSORS = (
	'django.core.context_processors.auth',
	'django.core.context_processors.debug',
	'django.core.context_processors.i18n',
	'django.core.context_processors.media',
	'context_processors.host',
	'context_processors.my_media_url',
)

TEMPLATE_DIRS = (
	# Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
	# Always use forward slashes, even on Windows.
	# Don't forget to use absolute paths, not relative paths.
	'/mnt/shares/lansite/templates',
)

INSTALLED_APPS = (
	'django.contrib.admin',
	'django.contrib.admindocs',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.databrowse',
	'django.contrib.sessions',
	'django.contrib.sites',
#	'gw',
#	'insupol',
#	'run1s',
#	'sro',
	'sro2',
	'todo',
)

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
#MEDIA_ROOT = ''
MEDIA_ROOT = '/mnt/shares/lansite/media/'
STATIC_DOC_ROOT = '/mnt/shares/lansite/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
#MEDIA_URL = ''
MEDIA_URL = '/lansite_media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

##################################################################################
# You can create local_settings.py to override the settings.
# It is recomended to put all your custom settings (database, path, etc.) there
# if you want to update from Subversion in future.
##################################################################################
try:
	from local_settings import *
except ImportError:
	pass
