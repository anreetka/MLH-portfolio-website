import unittest
import os
from peewee import *
from app import app, TimelinePost

os.environ['TESTING'] = 'true'

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