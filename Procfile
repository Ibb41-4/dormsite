#web: gunicorn dormsite.wsgi -b 0.0.0.0:$PORT
web: gunicorn_django -b 0.0.0.0:$PORT
celeryd: python manage.py celeryd -E -B --loglevel=INFO
