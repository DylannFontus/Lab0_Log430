# ADR 0002 – Séparation des responsabilités

## Statut
Acceptée

## Contexte
Afin de structurer le code de manière claire, maintenable et évolutive, il est essentiel de séparer les différentes responsabilités de l’application (présentation, logique, persistance).

## Décision
L’architecture de l’application suivra une séparation explicite en trois modules principaux, en cohérence avec les fichiers Django du projet :

1. **Présentation** : Les templates HTML (ex : `home.html`, `caisse.html`, etc.) et les vues Django (`views.py`) gèrent les interactions utilisateur (affichage, saisie, navigation).
2. **Logique** : Les services métiers (ex : `services/MagasinService.py`, `services/ProduitService.py`, `services/VenteService.py`, `services/StockService.py`) valident les opérations métier (vente, retour, consultation stock).
3. **Persistance** : Les modèles Django (`models.py`) fournissent un accès abstrait à la base de données MySQL via l’ORM.

## Raisons
- Favorise la lisibilité, la testabilité et la réutilisabilité du code.
- MVC souhaitable
- Permet de modifier ou remplacer une couche sans impacter les autres.
- Compatible avec les bonnes pratiques de développement logiciel (ex : séparation des préoccupations).
- Facilite l’évolution vers une architecture distribuée ou multi-niveaux dans les futurs laboratoires.

## Conséquences
- L’organisation des fichiers est structurée par module :  
  - Présentation : `templates/`, `views.py`, `urls.py`
  - Logique : `services/`
  - Persistance : `models.py`, `management/commands/initialise_db.py`
- Les tests unitaires sont centralisés dans `tests.py` et couvrent chaque couche.
- La couche de persistance reste découplée de la logique métier et de la présentation.