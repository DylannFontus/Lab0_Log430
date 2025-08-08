# ADR 0001 – Choix de la plateforme technologique

## Statut
Acceptée

## Contexte
Dans le cadre du développement d’un système de gestion de point de vente (POS) en architecture Django, je dois choisir une plateforme de développement adaptée à un environnement local, simple à mettre en œuvre, et compatible avec les besoins d’un projet modulaire et testable.

## Décision
J'ai choisi d’implémenter le projet en **Python** avec le framework **Django**, en utilisant **MySQL** comme système de gestion de base de données (SGBD) local.

## Raisons
- Python est un langage simple, expressif, et rapide à prototyper.
- Django est un framework web robuste, structurant, et bien adapté aux applications métiers.
- MySQL est un SGBD open-source largement répandu, stable et performant.
- L’ensemble du projet est facilement conteneurisable via Docker (`docker-compose.yml`), avec un service MySQL et un service Django.
- L’architecture Django permet une séparation claire entre les modèles (`models.py`), la logique métier (`services/`), les vues (`views.py`), et les templates HTML.
- Les tests automatisés sont facilités grâce à l’intégration native de Django (`tests.py`).
- L’initialisation de la base de données est automatisée via une commande de gestion (`management/commands/initialise_db.py`).

## Conséquences
- La couche de persistance utilisera les modèles Django (`models.py`).
- Le fichier `docker-compose.yml` inclura un service MySQL et un service Django.
- Les tests automatisés utiliseront le framework de test Django (`tests.py`).
- L’initialisation des données de base sera gérée par `initialise_db.py`.
- Les routes seront définies dans `urls.py` et la logique applicative dans `views.py` et `services/`.