# ADR 0005 – Implémentation de CQRS avec Event Broker

## Statut
Proposée

## Contexte
Dans le cadre de l'évolution vers une architecture microservices et l'adoption des patterns Event Sourcing (ADR 0004), il est nécessaire d'implémenter le pattern CQRS (Command Query Responsibility Segregation) pour le système de gestion de point de vente (POS). Cette séparation permettra de :
- Optimiser les performances en séparant les opérations de lecture et d'écriture
- Simplifier la complexité des modèles de données selon leur usage (command vs query)
- Faciliter la scalabilité indépendante des parties lecture et écriture
- Améliorer la cohérence avec l'Event Store Redis déjà en place
- Préparer l'architecture pour les sagas et workflows distribués

## Décision
Implémentation du pattern **CQRS avec Event Broker** utilisant **Redis Pub/Sub et Redis Streams** comme système de messagerie, réutilisant l'infrastructure Redis existante.

## Raisons
- **Séparation claire des responsabilités** : Commands pour les modifications d'état, Queries pour les lectures optimisées
- **Redis Pub/Sub + Streams** choisi pour réutiliser l'infrastructure Redis existante (ADR 0003 et ADR 0004)
- **Scalabilité indépendante** : possibilité de scaler séparément les microservices de commande et de lecture
- **Intégration native** : synergie parfaite avec l'Event Store Redis Streams déjà en place
- **Simplicité opérationnelle** : une seule technologie (Redis) pour cache, Event Store et messagerie
- **Performance** : Redis offre des performances élevées pour la messagerie en mémoire
- **Fonctionnalités complémentaires** :
  - Redis Pub/Sub pour la notification temps réel
  - Redis Streams pour la persistence et le replay des événements
  - Consumer Groups pour la distribution de charge
- **Compatibilité** : intégration Python native via `redis-py` déjà utilisé

## Conséquences
- **Modèles optimisés** : Write models pour les commandes, Read models pour les requêtes
- **Performance améliorée** : cache et indexes spécialisés pour les lectures
- **Évolutivité** : ajout facilité de nouvelles projections sans impact sur les commandes
- **Cohérence événementielle** : propagation automatique des changements via Redis Pub/Sub
- **Infrastructure simplifiée** : réutilisation de Redis pour tous les besoins de persistence et messagerie
- **Auditabilité** : traçabilité complète des commandes et événements via Redis Streams
- **Complexité réduite** : une seule technologie Redis au lieu de multiples systèmes
- **Cohérence éventuelle** : délai potentiel entre write et read models
- **Limitations de scalabilité** : Redis moins adapté que Kafka pour des volumes très élevés
- **Single point of failure** : dépendance accrue sur l'instance Redis

### Techniques
- **Command Side** :
  - Services Django dédiés (`CommandHandler`, `CommandDispatcher`)
  - Validation métier et persistance via Event Store Redis Streams
  - Publication d'événements vers Redis Pub/Sub après persistence
  
- **Query Side** :
  - Read models optimisés (vues matérialisées, projections)
  - Event handlers via Redis Pub/Sub subscribers
  - Reconstruction automatique des projections via Redis Streams replay
  
- **Infrastructure** :
  - Configuration Redis étendue pour Pub/Sub et Streams
  - Channels Redis organisés par aggregate/bounded context
  - Monitoring Redis via Prometheus/Grafana (extension ADR 0003)
  
- **Intégration** :
  - Handlers Django pour la souscription aux channels Redis
  - Serialization JSON des commands/events avec schémas versionnés
  - Gestion des erreurs et retry policies via Redis Consumer Groups
