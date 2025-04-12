import pika, ssl, time

context = ssl.create_default_context(cafile='certs/ca.crt')
context.load_cert_chain('certs/mes.crt', 'certs/mes.key')

params = pika.ConnectionParameters(
    host='rabbitmq',
    port=5671,
    ssl_options=pika.SSLOptions(context, 'rabbitmq')
)

connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='commands', durable=True)

for i in range(100):
    message = f"CMD_{i}"
    channel.basic_publish(
        exchange='',
        routing_key='commands',
        body=message,
        properties=pika.BasicProperties(delivery_mode=2)
    )
    print(f"[MES] Sent: {message}")
    time.sleep(0.1)

connection.close()
