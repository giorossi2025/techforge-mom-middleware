import pika, ssl, time
import pika, ssl, paho.mqtt.client as mqtt

context_rmq = ssl.create_default_context(cafile='certs/ca.crt')
context_rmq.load_cert_chain('certs/robot.crt', 'certs/robot.key')

params = pika.ConnectionParameters(
    host='rabbitmq',
    port=5671,
    ssl_options=pika.SSLOptions(context_rmq, 'rabbitmq')
)

connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='commands', durable=True)

mqtt_client = mqtt.Client()
mqtt_client.tls_set(ca_certs='certs/ca.crt', certfile='certs/robot.crt', keyfile='certs/robot.key')
mqtt_client.connect('mosquitto', 8883)

def callback(ch, method, properties, body):
    print(f"[Robot] Received: {body.decode()}")
    mqtt_client.publish("robot/status", payload=f"DONE:{body.decode()}", qos=1)
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue='commands', on_message_callback=callback)
print("[Robot] Waiting for commands...")
channel.start_consuming()
