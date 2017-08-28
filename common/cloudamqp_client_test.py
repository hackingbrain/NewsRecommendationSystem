""" Testing for CloudAMQP Client """
from cloudamqp_client import CloudAMQPClient

CLOUDAMQP_URL = "amqp://jrudocwa:wBPbbxjg8maWVvTFP-JRmmPpPRyxtoPr@donkey.rmq.cloudamqp.com/jrudocwa"
TEST_QUEUE_NAME = "test"


def test_basic():
    """ Method for testing basic """
    client = CloudAMQPClient(CLOUDAMQP_URL, TEST_QUEUE_NAME)
    sent_msg = {"test": "test"}
    client.send_message(sent_msg)
    received_msg = client.get_message()

    assert sent_msg == received_msg
    print 'test_basic passed'


if __name__ == '__main__':
    test_basic()
