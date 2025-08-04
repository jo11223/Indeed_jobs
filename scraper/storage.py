import json
from pymongo import MongoClient
from config import MONGO_URI, DB_NAME, COLLECTION


def save_to_json(jobs, filename="jobs.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(jobs, f, ensure_ascii=False, indent=2)


def save_to_mongo(jobs):
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    col = db[COLLECTION]
    if jobs:
        col.insert_many(jobs)