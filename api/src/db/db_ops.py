from pymongo.collection import Collection
from db.mongodb import get_database
from bson import ObjectId
from typing import Dict, List, Optional, Any

class DBOps:
    def __init__(self):
        self.db = get_database()

    def get_collection(self, collection_name: str) -> Collection:
        return self.db[collection_name]

    def get_one(self, collection_name: str, filters: Dict[str, any] = {}) -> Optional[Dict[str, Any]]:
        collection = self.get_collection(collection_name)
        result = collection.find_one(filters)
        if result and "_id" in result:
            result["_id"] = str(result["_id"])
        return result
    
    def get_many(self, collection_name: str, filters: Dict[str, any] = {}) -> List[Dict[str, Any]]:
        collection = self.get_collection(collection_name)
        result = List(collection.find(filters))
        for doc in result:
            doc["_id"] = str(result["_id"])
        return result
    
    def insert_one(self, collection_name: str, data: Dict[str, Any]) -> str:
        collection = self.get_collection(collection_name)
        result = collection.insert_one(data)
        return str(result.inserted_id)
    
    def insert_many(self, collection_name: str, data_list: List[Dict[str, Any]]) -> List[str]:
        collection = self.get_collection(collection_name)
        result = collection.insert_many(data_list)
        return [str(_id) for _id in result.inserted_ids]
    
    def update_one(self, collection_name: str, filters: Dict[str, Any], update_data: Dict[str, Any]) -> bool:
        collection = self.get_collection(collection_name)
        result = collection.update_one(filters, {"$set": update_data})
        return result.modified_count > 0
    
    def delete_one(self, collection_name: str, filters: Dict[str, Any]) -> bool:
        collection = self.get_collection(collection_name)
        result = collection.delete_one(filters)
        return result.deleted_count > 0
    
    def find_by_id(self, collection_name: str, id_str: str) -> Optional[Dict[str, Any]]:
        collection = self.get_collection(collection_name)
        try:
            obj_id = ObjectId(id_str)
        except Exception:
            return None
        result = collection.find_one({"_id": obj_id})
        if result:
            result["_id"] = str(result["_id"])
        return result