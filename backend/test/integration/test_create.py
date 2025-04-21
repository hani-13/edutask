import unittest
from src.util.dao import DAO
from bson import ObjectId
from pymongo import MongoClient
from pymongo.errors import OperationFailure
import os

class TestVideoDAO(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        mongo_url = os.getenv('MONGO_URL', 'mongodb://root:root@localhost:27017')
        try:
            cls.client = MongoClient(mongo_url)
            cls.db = cls.client['edutask']
            cls.temp_collection_name = "video_test"
            cls.dao = DAO(collection_name=cls.temp_collection_name)
            cls.dao.collection = cls.db[cls.temp_collection_name]
        except OperationFailure as e:
            print(f"MongoDB connection/authentication failed: {e}")
            raise e

    @classmethod
    def tearDownClass(cls):
        cls.db.drop_collection(cls.temp_collection_name)
        cls.client.close()

    def setUp(self):
        # Clear the temporary test collection before each test
        self.dao.collection.delete_many({})

    # === CREATE Tests ===

    def test_U1TC01_create_with_valid_data(self):
        """U1TC01: Valid input - should insert data correctly"""
        data = {"url": "https://www.youtube.com/watch?v=1"}
        result = self.dao.create(data)
        self.assertIsNotNone(result)
        self.assertIn('_id', result)

        inserted_id = ObjectId(result['_id'])
        found = self.dao.collection.find_one({'_id': inserted_id})
        self.assertIsNotNone(found)
        self.assertEqual(found['url'], data['url'])

    def test_U1TC02_create_with_missing_url_field(self):
        """U1TC02: Invalid input - missing 'url' field"""
        data = {"email": "test@gmail.com"}
        with self.assertRaises(Exception):
            self.dao.create(data)

    def test_U1TC03_create_with_empty_data(self):
        """U1TC03: Invalid input - empty JSON"""
        data = {}
        with self.assertRaises(Exception):
            self.dao.create(data)

    # === FIND_ONE Tests ===

    def test_U2TC01_findone_existing_id(self):
        """U2TC01: Valid ID - should return correct data"""
        data = {"url": "https://www.youtube.com/watch?v=1"}
        result = self.dao.create(data)
        inserted_id = ObjectId(result['_id'])

        found = self.dao.collection.find_one({'_id': inserted_id})
        self.assertIsNotNone(found)
        self.assertEqual(found['url'], data['url'])

    def test_U2TC02_findone_nonexistent_id(self):
        """U2TC02: Non-existent ID - should return None"""
        fake_id = ObjectId()
        found = self.dao.collection.find_one({'_id': fake_id})
        self.assertIsNone(found)


if __name__ == '__main__':
    unittest.main()
