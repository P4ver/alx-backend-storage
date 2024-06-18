#!/usr/bin/env python3
""" list all documents in python,"""

import pymongo


def list_all(mongo_collection):
    """ list all."""
    docs = mongo_collection.find()
    return [x for x in docs]
