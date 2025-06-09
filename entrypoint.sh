#!/bin/bash
set -e

echo "Contenu de /app :"
ls -l /app

echo "Contenu de /app/src :"
ls -l /app/src

echo "Contenu de /app/src/pos_django :"
ls -l /app/src/pos_django

python /app/src/pos_django/manage.py makemigrations --noinput
python /app/src/pos_django/manage.py migrate --noinput

exec python /app/src/pos_django/manage.py runserver 0.0.0.0:5000