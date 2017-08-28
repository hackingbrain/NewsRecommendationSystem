import datetime
import os
import sys

from dateutil import parser
from sklearn.feature_extraction.text import TfidfVectorizer

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client
from cloudamqp_client import CloudAMQPClient



DEDUPE_NEWS_TASK_QUEUE_URL = "amqp://roenklvc:tGRUWNEC3AuG7hH4ASr9_8uqCodGpdZT@donkey.rmq.cloudamqp.com/roenklvc"
DEDUPE_NEWS_TASK_QUEUE_NAME = "tap-news-dedupe-news-task-queue"

cloudamqp_client = CloudAMQPClient(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)

NEWS_TABLE_NAME = 'news-test'
SAME_NEWS_SIMILARITY_THRESHOLD = 0.9

SLEEP_TIME_IN_SECONDS = 1

def handle_message(msg):
    if msg is None or not isinstance(msg, dict):
        return
    task = msg
    text = task['text']
    if text is None:
        return

    published_at = parser.parse(task['publishedAt'])
    published_at_day_begin = datetime.datetime(published_at.year,
                                               published_at.month,
                                               published_at.day,
                                               0, 0, 0, 0)
    published_at_day_end = published_at_day_begin + datetime.timedelta(days=1)

    db = mongodb_client.get_db()
    same_day_news_list = list(db[NEWS_TABLE_NAME].find(
        {'publishedAt':
         {'$gte': published_at_day_begin, '$lt': published_at_day_end}}))

    if same_day_news_list is not None and len(same_day_news_list) > 0:
        documents = [news['text'] for news in same_day_news_list]
        documents.insert(0,text)

        tfidf = TfidfVectorizer().fit_transform(documents)
        pairwise_sim = tfidf*tfidf.T

        print pairwise_sim

        rows, _ = pairwise_sim.shape 
        for row in range(1, rows):
            if pairwise_sim[row, 0] > SAME_NEWS_SIMILARITY_THRESHOLD:
                print "duplicate news. Skip."
                return 
    task['publishedAt'] = parser.parse(task['publishedAt'])
    db[NEWS_TABLE_NAME].replace_one({'digest': task['digest']}, task, upsert=True)

while True:
    if cloudamqp_client is not None:
        msg = cloudamqp_client.get_message()
        if msg is not None:
            try:
                handle_message(msg)
            except Exception as e:
                print e

        cloudamqp_client.sleep(SLEEP_TIME_IN_SECONDS)
