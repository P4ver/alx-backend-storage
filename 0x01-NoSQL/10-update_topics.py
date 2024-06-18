#!/usr/bin/env python3
""" Change school topics,"""


def update_topics(mongo_collection, name, topics):
    """ update_topics,"""
    qry = {"name": name}
    new_val = {"$set": {"topics": topics}}
    mongo_collection.update_many(qry, new_val)
