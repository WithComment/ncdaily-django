release: python manage.py migrate
web: gunicorn ncdaily.wsgi
clock: python app/clock.py