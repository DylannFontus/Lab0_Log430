# ADR 0004 – Ajout d'un Event Store avec Redis

## Statut
Proposée

## Contexte
Pour l'évolution vers une architecture microservices et l'implémentation de patterns Event Sourcing et CQRS, il est nécessaire d'ajouter un système de stockage d'événements (Event Store) au système de gestion de point de vente (POS). L'Event Store doit permettre de :
- Persister tous les événements métier de manière séquentielle et immuable
- Supporter la reconstruction d'état (replay) à partir de l'historique des événements
- Faciliter la mise en œuvre de sagas orchestrées et chorégraphiées
- Assurer la traçabilité complète des opérations métier
- S'intégrer facilement avec l'infrastructure existante (Docker, Django, MySQL)

## Décision
**Redis Streams** a été retenu comme Event Store pour le système POS, complétant l'utilisation existante de Redis comme cache.

## Raisons
- **Redis Streams** offre nativement les fonctionnalités d'Event Store (append-only, ordering, persistence)
- **Intégration simplifiée** : Redis est déjà présent dans l'architecture pour le cache (ADR 0003)
- **Performance** : Redis Streams permet un débit élevé pour l'écriture et la lecture d'événements
- **Durabilité** : Support de la persistence sur disque (RDB + AOF) pour garantir la non-perte d'événements
- **Fonctionnalités avancées** :
  - Consumer Groups pour la distribution de charge
  - Range queries pour le replay d'événements
  - Support natif des streams avec Python via `redis-py`
- **Scalabilité** : Possibilité de sharding et clustering Redis pour volumes importants
- **Simplicité opérationnelle** : Réutilisation des compétences et outils de monitoring Redis existants

## Conséquences
- Les événements métier seront stockés de manière persistante et ordonnée dans Redis Streams
- Implémentation facilitée des patterns Event Sourcing et CQRS
- Reconstruction d'état possible via replay des événements historiques
- Support natif pour les sagas et workflows distribués
- Intégration transparente avec Django via `django-redis` et `redis-py`
- Monitoring unifié via Prometheus/Grafana (métriques Redis existantes étendues)
- Complexité accrue de l'architecture avec l'ajout du concept d'Event Store
- Nécessité de gérer la cohérence entre l'état traditionnel (MySQL) et l'Event Store
- Formation requise sur les concepts Event Sourcing/CQRS pour l'équipe de développement
- Stratégie de rétention des événements à définir pour éviter la croissance infinie

### Techniques
- Configuration Redis étendue pour supporter les Streams avec persistence AOF
- Ajout de services Django pour la gestion des événements (`EventStoreService`, `EventPublisher`)
- Implémentation d'aggregate roots et d'événements métier typés
- Extension du monitoring Prometheus pour inclure les métriques Event Store
- Tests automatisés pour la cohérence événementielle et les scénarios de replay
