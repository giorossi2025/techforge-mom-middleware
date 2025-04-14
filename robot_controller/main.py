import pika
import ssl
import yaml
import json
import paho.mqtt.client as mqtt

# Carica la configurazione da YAML
with open("robot_controller/config.yml", "r") as file:
    config = yaml.safe_load(file)

rabbit_cfg = config["rabbitmq"]
mqtt_cfg = config["mqtt"]
certs = rabbit_cfg["certs"]

# TLS RabbitMQ
context = ssl.create_default_context(cafile=certs["ca"])
context.load_cert_chain(certs["cert"], certs["key"])

# Connessione a RabbitMQ
params = pika.ConnectionParameters(
    host=rabbit_cfg["host"],
    port=rabbit_cfg["port"],
    ssl_options=pika.SSLOptions(context)
)

connection = pika.BlockingConnection(params)
channel = connection.channel()

def on_message(ch, method, properties, body):
    data = json.loads(body)
    print(f"[Robot] Comando ricevuto: {data['type']} da {data['machine_id']}")

    response = {
        "status": "OK",
        "machine_id": data["machine_id"]
    }

    mqtt_client.publish(mqtt_cfg["topic"], json.dumps(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue=rabbit_cfg["queue"], on_message_callback=on_message)

# Configurazione client MQTT con TLS
mqtt_client = mqtt.Client()
mqtt_client.tls_set(
    ca_certs=mqtt_cfg["certs"]["ca"],
    certfile=mqtt_cfg["certs"]["cert"],
    keyfile=mqtt_cfg["certs"]["key"]
)
mqtt_client.connect(mqtt_cfg["host"], mqtt_cfg["port"], 60)

print("[Robot] In ascolto...")
channel.start_consuming()
