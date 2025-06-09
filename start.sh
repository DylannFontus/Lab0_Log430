#!/bin/bash
set -e

echo "Attente de la base de données MySQL..."
until mysqladmin ping -h "$DB_HOST" -u"$DB_USER" -p"$DB_PASSWORD" --silent; do
  sleep 2
done

echo "Base de données MySQL disponible."

# Se placer dans le dossier où se trouve manage.py
cd /app/src/pos_django

echo "Création des migrations si nécessaire..."
python manage.py makemigrations magasin

echo "Application des migrations..."
python manage.py migrate

echo "Initialisation de la base de données avec Django ORM..."
python manage.py initialise_db

echo "Démarrage du serveur Django sur 0.0.0.0:5000"
python manage.py runserver 0.0.0.0:5000
