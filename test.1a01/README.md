# test.1a01

Test for [test](https://fabrique.studio)

## Requirements

- Python 3.6+
- Django 2.2.10+
- Django REST Framework

## Installation

1. Download code
2. Prepare `local-settings.py` like [sample](docs/local-settings.py)
3. Init Django data:
   ```bash
   ./manage.py migrate
   ./manage.py createsuperuser
   ```
4. Run:
   - Production:
      - prepare `/etc/httpd/conf.d/test.conf` like [sample](docs/httpd.conf) for Apache
      - `systemctl restart httpd`
   - Development: `./manage.py run`

## Tests

You can load [fixtures](test.1a01/polls/fixtures/) to init test data.  
Then try to `curl` tests (URLs for `manage.py runserver` mode below): :

- [get active polls](http://localhost:8000/rest/p/)
- [get questions of poll #1](http://localhost:8000/rest/p/1/)
- [add answers](http://localhost:8000/rest/p/) - POST, use [samples](samples/)
- [get votes (polls that customer partisipate in) of customer id=1](http://localhost:8000/rest/v/1/)
- [get its answers in poll #1](http://localhost:8000/rest/v/1/1/)

`curl` usage example:
- get: `curl -H 'Accept: application/json; indent=2' http://127.0.0.1:8000/rest/...`
- post: `curl -X POST  http://127.0.0.1:8000/rest/a/ -H 'Content-Type: application/json' -d @file.json`

## REST API documentation

OpenAPI [schema](docs/openapi-schema.yml) can be comfortable explored in [Swagger Editor](https://editor.swagger.io)
or other UI schema viewer.