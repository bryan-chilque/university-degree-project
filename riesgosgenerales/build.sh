#!/bin/sh
set -o errexit
pip install -r requirements.txt
pip install psycopg2-binary
python manage.py collectstatic --no-input
python manage.py migrate
