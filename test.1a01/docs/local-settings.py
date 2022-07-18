"""Local settings
Put it near `settings.py`
"""
DEBUG = False
SECRET_KEY = 'verysecretkey'
DATABASES = {
    'default': {  # anything on your choice
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/var/lib/test/db.sqlite3',
    }
}
ALLOWED_HOSTS = ['0.0.0.0']
