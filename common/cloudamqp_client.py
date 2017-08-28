""" CloudAMQP Client """
import json
import pika


class CloudAMQPClient(object):
    """ Class for creating a CloudAMQP Client"""

    def __init__(self, cloud_amqp_url, queue_name):
        self.cloud_amqp_url = cloud_amqp_url
        self.queue_name = queue_name
        self.params = pika.URLParameters(cloud_amqp_url)
        self.params.socket_time_timeout = 3
        self.connection = pika.BlockingConnection(self.params)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue_name)

    def send_message(self, message):
        """ Method for sending message """
        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue_name,
            body=json.dumps(message))
        print '[x] Sent message to %s: %s' % (self.queue_name, message)

    def get_message(self):
        """ Method for retrieving message """
        method_frame, _, body = self.channel.basic_get(
            self.queue_name)
        if method_frame:
            print '[x] Received message from %s: %s' % (self.queue_name, body)
            self.channel.basic_ack(method_frame.delivery_tag)
            return json.loads(body)
        else:
            print 'no message returned'

    # (this function is import) BlockingConnection.sleep is a safer way to sleep than time.sleep()
    def sleep(self, seconds):
        """ Method for defining sleep time """
        self.connection.sleep(seconds)
