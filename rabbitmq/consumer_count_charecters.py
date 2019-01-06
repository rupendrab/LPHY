import logging
import pika
import sys
import argparse

from consumer_from_queue import QueueConsumer

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)

class QueueConsumerCountChars(QueueConsumer):

    def process_message(self, body):
        print(len(body))

def main(parsed):
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    consumer = QueueConsumerCountChars(amqp_url = parsed.url,
        exchange_name = parsed.ex,
        exchange_type = parsed.type,
        queue_name = parsed.queue
    )
    try:
        consumer.run()
    except KeyboardInterrupt:
        consumer.stop()

if __name__ == '__main__':
    from sys import argv
    parser = argparse.ArgumentParser()
    parser.add_argument("url",
                        help=r'AMQP URL: e.g. amqp://guest:guest@localhost:5672/<Exchange Name>')
    parser.add_argument("-ex",
                        help="Exchange Name",
                        required=True)
    parser.add_argument("-type", 
                        help="Exchange Type",
                        required=True)
    parser.add_argument("-queue",
                        help="Queue Name",
                        required=True)
    # print(argv)
    parsed = parser.parse_args(argv[1:])
    if not parsed:
        sys.exit(1)
    main(parsed)
