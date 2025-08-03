# cspell:ignore gunicorn wsgi

web: gunicorn online_voting_system.wsgi --log-file - --bind 0.0.0.0:$PORT
release: python manage.py migrate && python manage.py collectstatic --noinput
