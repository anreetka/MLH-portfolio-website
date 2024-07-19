import unittest
import os
from peewee import SqliteDatabase
from app import app, TimelinePost

os.environ['TESTING'] = 'true'

MODELS = [TimelinePost]

test_db = SqliteDatabase(':memory:')

class TestTimelinePost(unittest.TestCase):  # Corrected the spelling of 'Testcase' to 'TestCase'
    def setUp(self):
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        test_db.connect()
        test_db.create_tables(MODELS)

    def tearDown(self):
        test_db.drop_tables(MODELS)
        test_db.close()

    def test_timeline_post(self):
        first_post = TimelinePost.create(name='John Doe', email='john@example.com', content='Hello world, I\'m John!')
        self.assertEqual(first_post.id, 1)
        second_post = TimelinePost.create(name='Jane Doe', email='jane@example.com', content='Hello world, I\'m Jane!')
        self.assertEqual(second_post.id, 2)

if __name__ == '__main__':
    unittest.main()

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        #assert "<title>MLH Fellow</title>" in html

    def test_timeline(self):
        response = self.client.get("api/timeline_post")
        self.assertEqual(response.status_code, 200)
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        self.assertEqual(len(json["timeline_posts"]), 0)

    def test_malformed_timeline_post(self):
        response = self.client.post("/api/timeline_post", data={"email": "john@example.com",
        "content": "Hello world, I'm John"})
        self.assertEqual(response.status_code, 400)
        html = response.get_data(as_text=True)
        self.assertIn("Invalid name", html)

        response = self.client.post("/api/timeline_post", data={"email": "john@example.com",
        "content": "", "name": "John Doe"})
        self.assertEqual(response.status_code, 400)
        html = response.get_data(as_text=True)
        self.assertIn("Invalid content", html)

        response = self.client.post("/api/timeline_post", data={"email": "not-an-email",
        "content": "Hello world, I'm John", "name": "John Doe"})
        self.assertEqual(response.status_code, 400)
        html = response.get_data(as_text=True)
        self.assertIn("Invalid email", html)