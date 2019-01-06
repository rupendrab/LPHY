import pika
import sys

def show_usage():
    sys.stderr.write("Usage: %s <Queue Name> \n" % sys.argv[0])

if (len(sys.argv) != 2):
    show_usage()
    sys.exit(1)

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='direct_logs',
                         exchange_type='direct')

queue_name = sys.argv[1]
result = channel.queue_declare(queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()
