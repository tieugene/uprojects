# test.1b19
Test for [TL](https://cpa.tl)

## Requirements
- Python 3.7+
- [Django](https://www.djangoproject.com) 3.2
- [Django REST Framework](https://github.com/encode/django-rest-framework/)
- [django-admirarchy](https://github.com/idlesign/django-admirarchy) *(optional)*

*Note: to disable `django-admirarchy` delete it in [INSTALLED_APPS](tidemo/setting.py) and [core/admin.py](tidemo/core/admin.py)*

## Install and setup
- `manage.py ...`:
  - `migrate`
  - `createsuperuser --username admin --email admin@nowhere.net`
  - `loaddata --app core org depart person`

## Test

DRF: http://localhost:8000/rest/
