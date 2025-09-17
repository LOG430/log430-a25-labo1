"""
User DAO (MongoDB)
SPDX-License-Identifier: LGPL-3.0-or-later
"""
import os
import sys
from typing import List, Optional
from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient, ReturnDocument
from pymongo.collection import Collection

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.user import User


class UserDAOMongo:
    def __init__(self):
        env_file = find_dotenv()
        if env_file:
            load_dotenv(env_file)

        # Use localhost for local testing, mongo for Docker
        host = os.getenv("MONGODB_HOST", "localhost")
        if host == "mongo":
            # If running locally but env says mongo, use localhost
            try:
                # Try to connect to localhost first for local testing
                test_client = MongoClient("mongodb://user:pass@localhost:27017", serverSelectionTimeoutMS=1000)
                test_client.server_info()
                host = "localhost"
                test_client.close()
            except:
                host = "mongo"  # Keep original if localhost fails
        
        username = os.getenv("DB_USERNAME", "user")
        password = os.getenv("DB_PASSWORD", "pass")
        db_name = os.getenv("MONGODB_DB_NAME", "store")

        # MongoDB connection with authentication
        if username and password:
            self.client = MongoClient(f"mongodb://{username}:{password}@{host}:27017")
        else:
            self.client = MongoClient(f"mongodb://{host}:27017")
            
        self.db = self.client[db_name]
        self.users: Collection = self.db["users"]
        self.counters: Collection = self.db["counters"]

        self.counters.update_one(
            {"_id": "users"},
            {"$setOnInsert": {"seq": 0}},
            upsert=True,
        )

    def _next_id(self) -> int:
        doc = self.counters.find_one_and_update(
            {"_id": "users"},
            {"$inc": {"seq": 1}},
            return_document=ReturnDocument.AFTER,
        )
        return int(doc["seq"])

    def select_all(self) -> List[User]:
        docs = self.users.find({}, {"_id": 1, "name": 1, "email": 1}).sort("_id", 1)
        return [User(int(d["_id"]), d.get("name"), d.get("email")) for d in docs]

    def insert(self, user: User) -> int:
        new_id = self._next_id()
        self.users.insert_one({"_id": new_id, "name": user.name, "email": user.email})
        return new_id

    def update(self, user: User) -> int:
        res = self.users.update_one(
            {"_id": int(user.id)},
            {"$set": {"name": user.name, "email": user.email}},
        )
        return res.modified_count

    def delete(self, user_id: int) -> int:
        res = self.users.delete_one({"_id": int(user_id)})
        return res.deleted_count

    def delete_all(self) -> int:
        res = self.users.delete_many({})
        return res.deleted_count

    def close(self):
        self.client.close()
