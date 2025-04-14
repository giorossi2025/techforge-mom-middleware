import pika
import ssl
import json
import yaml
from datetime import datetime

# Carica configurazione da file YAML
with open("mes_simulator/config.yml", "r") as file:
    config = yaml.safe_load(file)

rabbit_cfg = config["rabbitmq"]
certs = rabbit_cfg["certs"]

# Contesto TLS
context = ssl.create_default_context(cafile=certs["ca"])
context.load_cert_chain(certs["cert"], certs["key"])

params = pika.ConnectionParameters(
    host=rabbit_cfg["host"],
    port=rabbit_cfg["port"],
    ssl_options=pika.SSLOptions(context)
)

connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue=rabbit_cfg["queue"], durable=True)

# Messaggio
command = {
    "type": "START_CYCLE",
    "timestamp": datetime.utcnow().isoformat(),
    "machine_id": "RBT_001"
}

channel.basic_publish(
    exchange='',
    routing_key=rabbit_cfg["queue"],
    body=json.dumps(command),
    properties=pika.BasicProperties(delivery_mode=2)
)

print("[MES] Comando inviato")
connection.close()
