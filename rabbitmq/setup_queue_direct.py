import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

def show_usage():
    sys.stderr.write("Usage: %s <Queue Name> [info] [warning] [error]\n" % sys.argv[0])

if (len(sys.argv) < 3):
    show_usage()
    sys.exit(1)

queue_name = sys.argv[1]

if not queue_name:
    show_usage()
    sys.exit(1)

severities = sys.argv[2:]
if not severities:
    show_usage()
    sys.exit(1)

channel.exchange_declare(exchange='direct_logs',
                         exchange_type='direct')

result = channel.queue_declare(queue=queue_name)

for severity in severities:
    channel.queue_bind(exchange='direct_logs',
                       queue=queue_name,
                       routing_key=severity)

channel.close()
connection.close()
