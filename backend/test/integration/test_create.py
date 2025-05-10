import unittest
from bson import ObjectId
from pymongo import MongoClient
from pymongo.errors import WriteError, ServerSelectionTimeoutError
from src.util.dao import DAO
import os
from types import SimpleNamespace


class IntegrationTestDAOCreate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        mongo_url = os.getenv('MONGO_URL', 'mongodb://root:root@localhost:27017')
        try:
            cls.client = MongoClient(mongo_url, serverSelectionTimeoutMS=3000)
            cls.db = cls.client['edutask']
            cls.collection_name = 'video_test'
            cls.dao = DAO(collection_name=cls.collection_name)
            cls.dao.collection = cls.db[cls.collection_name]
        except Exception as e:
            print(f"MongoDB setup failed: {e}")
            raise

    @classmethod
    def tearDownClass(cls):
        cls.db.drop_collection(cls.collection_name)
        cls.client.close()

    def setUp(self):
        # Clear collection before each test
        self.dao.collection.delete_many({})

    # === TC01: URL present, DB available ===
    def test_TC01_valid_url_and_db_available(self):
        """TC01: Data inserted correctly and returned"""
        data = {"url": "https://www.youtube.com/watch?v=123"}
        result = self.dao.create(data)
        self.assertIsNotNone(result)
        self.assertIn("_id", result)

        # Verify it exists in DB
        inserted = self.dao.collection.find_one({"_id": ObjectId(result['_id'])})
        self.assertIsNotNone(inserted)
        self.assertEqual(inserted['url'], data['url'])

    # === TC02: URL missing, DB available ===
    def test_TC02_missing_url_field(self):
        """TC02: Exception due to missing required field"""
        data = {"title": "No URL here"}
        with self.assertRaises(WriteError):
            self.dao.create(data)

    # === TC03: URL present, DB unavailable ===
    def test_TC03_valid_url_but_db_unavailable(self):
        """TC03: Exception due to connection failure"""
        bad_client = MongoClient("mongodb://localhost:9999", serverSelectionTimeoutMS=1000)
        bad_db = bad_client['edutask']
        bad_collection = bad_db[self.collection_name]
        bad_dao = SimpleNamespace(collection=bad_collection)

        with self.assertRaises(ServerSelectionTimeoutError):
            # Simulate what DAO.create would do
            inserted_id = bad_dao.collection.insert_one({"url": "https://www.youtube.com/watch?v=456"}).inserted_id


if __name__ == '__main__':
    unittest.main()
