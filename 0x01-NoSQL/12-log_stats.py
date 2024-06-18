#!/usr/bin/env python3
""" Log stats,"""


from pymongo import MongoClient


def display_log_stats():
    """ display_log_stats,"""
    mongo_client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_logs = mongo_client.logs.nginx
    total_logs = nginx_logs.count_documents({})
    get_requests = nginx_logs.count_documents({"method": "GET"})
    post_requests = nginx_logs.count_documents({"method": "POST"})
    put_requests = nginx_logs.count_documents({"method": "PUT"})
    patch_requests = nginx_logs.count_documents({"method": "PATCH"})
    delete_requests = nginx_logs.count_documents({"method": "DELETE"})
    status_checks = nginx_logs.count_documents(
        {"method": "GET", "path": "/status"})
    print(f"{total_logs} logs")
    print("Methods:")
    print(f"\tmethod GET: {get_requests}")
    print(f"\tmethod POST: {post_requests}")
    print(f"\tmethod PUT: {put_requests}")
    print(f"\tmethod PATCH: {patch_requests}")
    print(f"\tmethod DELETE: {delete_requests}")
    print(f"{status_checks} status check")


if __name__ == "__main__":
    display_log_stats()
