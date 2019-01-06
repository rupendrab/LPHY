import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    time.sleep(body.count(b'.'))
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)

if __name__ == '__main__':
    print(" [*] Waiting for message, to exit precc CTRL+C")
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(callback, queue='task_queue')
    channel.start_consuming()

