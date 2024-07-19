import unittest
from unittest.mock import patch, MagicMock
from app import app, TimelinePost
from playhouse.shortcuts import model_to_dict
from peewee import DoesNotExist
import os

os.environ['TESTING'] = 'true'

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)

    def test_home_content(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn("Anreet Kaur", html)
        self.assertIn("Technical Skills", html)
        self.assertIn("Work Experiences", html)
        self.assertIn("Education", html)

    @patch('app.TimelinePost.select')
    def test_timeline(self, mock_select):
        mock_select.return_value.order_by.return_value = []

        response = self.client.get("/api/timeline_post")
        self.assertEqual(response.status_code, 200)
        json = response.get_json()
        self.assertIn("timeline_posts", json)
        self.assertEqual(len(json["timeline_posts"]), 0)


    @patch('app.TimelinePost.select')
    def test_get_timeline_empty(self, mock_select):
        mock_select.return_value.order_by.return_value = []

        response = self.client.get("/api/timeline_post")
        self.assertEqual(response.status_code, 200)
        json = response.get_json()
        self.assertIn("timeline_posts", json)
        self.assertEqual(len(json["timeline_posts"]), 0)

    @patch('app.model_to_dict')
    @patch('app.TimelinePost.create')
    def test_create_timeline_post(self, mock_create, mock_model_to_dict):
        mock_post = MagicMock()
        mock_post.name = 'John Doe'
        mock_post.email = 'john@example.com'
        mock_post.content = 'This is a test post'
        mock_post.id = 1
        mock_create.return_value = mock_post
        mock_model_to_dict.return_value = {
            "name": "John Doe",
            "email": "john@example.com",
            "content": "This is a test post"
        }

        response = self.client.post("/api/timeline_post", data={
            "name": "John Doe",
            "email": "john@example.com",
            "content": "This is a test post"
        })

        self.assertEqual(response.status_code, 200)
        json = response.get_json()
        self.assertIsNotNone(json)
        self.assertIn("name", json)
        self.assertEqual(json["name"], "John Doe")
        self.assertIn("email", json)
        self.assertEqual(json["email"], "john@example.com")
        self.assertIn("content", json)
        self.assertEqual(json["content"], "This is a test post")

    def test_malformed_timeline_post(self):
        response = self.client.post("/api/timeline_post", data={
            "name": "",
            "email": "john@example.com",
            "content": "This is a test post"
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid name", response.get_data(as_text=True))

        response = self.client.post("/api/timeline_post", data={
            "name": "John Doe",
            "email": "john@example.com",
            "content": ""
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid content", response.get_data(as_text=True))

        response = self.client.post("/api/timeline_post", data={
            "name": "John Doe",
            "email": "johnexample.com",
            "content": "This is a test post"
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid email", response.get_data(as_text=True))