""" Mongo Client """
from pymongo import MongoClient

MONGO_DB_HOST = 'localhost'
MONGO_DB_PORT = '27017'
DB_NAME = 'tap-news'
CLIENT = MongoClient("%s:%s" % (MONGO_DB_HOST, MONGO_DB_PORT))


def get_db(database=DB_NAME):
    """ Method for getting database"""
    return CLIENT[database]
