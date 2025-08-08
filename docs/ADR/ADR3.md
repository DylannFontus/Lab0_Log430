# ADR 0003 – Choix des technologies de supervision, cache et monitoring

## Statut
Acceptée

## Contexte
Pour garantir la performance, la scalabilité et la supervision du système de gestion de point de vente (POS) développé sous Django, il est nécessaire d’intégrer des outils de monitoring, de test de charge et de cache. Ces outils doivent s’intégrer facilement à l’architecture existante basée sur Docker, Python/Django et MySQL, tout en respectant les bonnes pratiques DevOps.

## Décision
Les technologies suivantes ont été retenues :

- **k6** pour les tests de charge et de performance.
- **NGINX** comme reverse proxy HTTP devant l’application Django.
- **Grafana** pour la visualisation des métriques et des logs.
- **Prometheus** pour la collecte et l’agrégation des métriques applicatives et système.
- **Redis** comme système de cache distribué pour Django.

## Raisons
- **k6** permet de simuler des charges réalistes et de valider la robustesse de l’application sous contrainte.
- **NGINX** est un reverse proxy performant, couramment utilisé pour sécuriser, équilibrer et optimiser le trafic HTTP.
- **Prometheus** s’intègre facilement avec Django (via `django-prometheus`) et permet de collecter des métriques détaillées sur l’application et l’infrastructure.
- **Grafana** offre des tableaux de bord puissants pour visualiser en temps réel les métriques issues de Prometheus.
- **Redis** améliore la performance de l’application Django (sessions, cache, files d’attente) et s’intègre nativement avec Django via `django-redis`.

## Conséquences
- Les métriques applicatives et système seront exposées à Prometheus et visualisées dans Grafana.
- Les performances de l’application seront validées régulièrement via des scénarios k6.
- NGINX servira de point d’entrée unique, améliorant la sécurité et la gestion du trafic.
- Redis sera utilisé pour le cache Django, réduisant la charge sur la base de données et accélérant les réponses.
- L’ensemble de ces outils sera orchestré via Docker Compose pour garantir la portabilité et la reproductibilité de l’environnement.