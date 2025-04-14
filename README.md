# Middleware Industrial Prototype

Prototipo funzionante di un middleware asincrono e sicuro per l’integrazione tra un sistema MES e un robot industriale, basato su RabbitMQ e MQTT con supporto TLS e autenticazione a certificati X.509.

## Obiettivi del progetto

- Abilitare comunicazione asincrona tra sistemi eterogenei (MES → Robot)
- Garantire integrità, autenticazione e riservatezza tramite TLS
- Simulare flussi real-time e fault recovery
- Dimostrare la scalabilità e modularità in un contesto Industry 4.0

## Componenti

- `mes_simulator/`  
  Simula un sistema MES che invia comandi via RabbitMQ (TLS).
  
- `robot_controller/`  
  Riceve comandi dalla coda RabbitMQ e invia risposte MQTT (TLS).

- `rabbitmq/`  
  Contiene configurazioni predefinite (`definitions.json`) e certificati server TLS.

## Sicurezza implementata

- TLS 1.3 per RabbitMQ e MQTT
- Autenticazione mutua con certificati X.509
- Code durabili e consegna garantita (at-least-once)
- Controllo accessi RBAC per utenti `mes_user` e `robot_user`

## Requisiti

- Docker + Docker Compose
- Python 3.11
- Librerie Python:
  - `pika` (RabbitMQ)
  - `paho-mqtt` (MQTT)
  - `pyyaml`, `ssl`, `json`

## Esecuzione

1. Avviare RabbitMQ via Docker Compose:
   ```bash
   docker-compose up -d
