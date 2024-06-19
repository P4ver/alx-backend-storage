#!/usr/bin/env python3
""" 12. Log stats
"""

from pymongo import MongoClient


def log_stats():
    """ log_stats.
    """
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs_collection = client.logs.nginx
    
    total = logs_collection.count_documents({})
    
    if total == 0:
        print(f"{total} logs")
        print("Methods:")
        print(f"\tmethod GET: 0")
        print(f"\tmethod POST: 0")
        print(f"\tmethod PUT: 0")
        print(f"\tmethod PATCH: 0")
        print(f"\tmethod DELETE: 0")
        print(f"0 status check")
        return

    get = logs_collection.count_documents({"method": "GET"})
    post = logs_collection.count_documents({"method": "POST"})
    put = logs_collection.count_documents({"method": "PUT"})
    patch = logs_collection.count_documents({"method": "PATCH"})
    delete = logs_collection.count_documents({"method": "DELETE"})
    path = logs_collection.count_documents(
        {"method": "GET", "path": "/status"})
    
    print(f"{total} logs")
    print("Methods:")
    print(f"\tmethod GET: {get}")
    print(f"\tmethod POST: {post}")
    print(f"\tmethod PUT: {put}")
    print(f"\tmethod PATCH: {patch}")
    print(f"\tmethod DELETE: {delete}")
    print(f"{path} status check")

if __name__ == "__main__":
    log_stats()
