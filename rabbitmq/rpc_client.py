import pika
import uuid
from collections import OrderedDict

class FibonacciRpcClient(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)
        self.responses = OrderedDict()
        self.requests_sent = 0
        self.responses_received = 0

    def on_response(self, ch, method, props, body):
        """
        if self.corr_id == props.correlation_id:
           self.response = body
        """
        self.responses[int(props.correlation_id)] = int(body)
        self.responses_received += 1

    def call(self, n):
        self.response = None
        # self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue',
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = str(n)
                                         ),
                                   body=str(n))
        self.requests_sent += 1
        """
        while self.response is None:
            self.connection.process_data_events()
        return int(self.response)
        """

    def wait_until_all_responses(self):
        while (self.requests_sent > self.responses_received):
            self.connection.process_data_events()

    def show_responses(self):
        for (num, fib_num) in self.responses.items():
            print("%d: %d" % (num, fib_num))

if __name__ == '__main__':
    import sys
    from sys import argv
    if len(argv) < 2:
        sys.exit(0)
    fibonacci_rpc = FibonacciRpcClient()
    for val in argv[1:]:
        print(" [x] Requesting fib(%d)" % int(val))
        fibonacci_rpc.call(val)
        # print(" [.] Got %r" % response)
    fibonacci_rpc.wait_until_all_responses()
    fibonacci_rpc.show_responses()
