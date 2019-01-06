import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

def show_usage():
    sys.stderr.write("Usage: %s <Queue Name> [type 1] [type 2] .... \n" % sys.argv[0])

if (len(sys.argv) < 3):
    show_usage()
    sys.exit(1)

queue_name = sys.argv[1]

if not queue_name:
    show_usage()
    sys.exit(1)

binding_keys = sys.argv[2:]
if not binding_keys:
    show_usage()
    sys.exit(1)

channel.exchange_declare(exchange='topic_logs',
                         exchange_type='topic')

result = channel.queue_declare(queue=queue_name)

for binding_key in binding_keys:
    channel.queue_bind(exchange='topic_logs',
                       queue=queue_name,
                       routing_key=binding_key)

channel.close()
connection.close()
