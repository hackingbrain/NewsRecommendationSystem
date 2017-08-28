import os
import sys

from newspaper import Article

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'scrapers'))

import cnn_news_scraper
from cloudamqp_client import CloudAMQPClient

# TODO: use your own queue.
SCRAPE_NEWS_TASK_QUEUE_URL = "amqp://jrudocwa:wBPbbxjg8maWVvTFP-JRmmPpPRyxtoPr@donkey.rmq.cloudamqp.com/jrudocwa"
SCRAPE_NEWS_TASK_QUEUE_NAME = "tap-news-scrape-news-task-queue"
DEDUPE_NEWS_TASK_QUEUE_URL = "amqp://roenklvc:tGRUWNEC3AuG7hH4ASr9_8uqCodGpdZT@donkey.rmq.cloudamqp.com/roenklvc"
DEDUPE_NEWS_TASK_QUEUE_NAME = "tap-news-dedupe-news-task-queue"

SLEEP_TIME_IN_SECONDS = 5

dedupe_news_queue_client = CloudAMQPClient(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)
scrape_news_queue_client = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)


SLEEP_TIME_IN_SECONDS = 5
def handle_message(msg):
    if msg is None or not isinstance(msg, dict):
        print 'msg is broken'
        return 

    task = msg 
    text = None

    # if task['source'] == 'cnn':
    #     print 'scraping CNN news'
    #     text = cnn_news_scraper.extract_news(task['url'])
    # else:
    #     print "News source [%s] not supported." % task['source']

    article = Article(task['url'])
    article.download()
    article.parse()

    
    #task['text'] = text
    task['text'] = article.text.encode('utf-8')
    dedupe_news_queue_client.send_message(task)

while True:
    if scrape_news_queue_client is not None:
        msg = scrape_news_queue_client.get_message()
        if msg is not None:
            try:
                handle_message(msg)
            except Exception as e:
                print 
                pass
        scrape_news_queue_client.sleep(SLEEP_TIME_IN_SECONDS)