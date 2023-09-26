#!/usr/bin/env bash
# exit on error
set -o errexit

pip3 install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py makemigrations
python manage.py migrate
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('xeland314', 'alexpila.314@gmail.com', 'indrod_group_pass')"