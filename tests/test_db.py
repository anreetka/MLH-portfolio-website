import unittest
import os
from peewee import SqliteDatabase
from app import app, TimelinePost
from playhouse.shortcuts import model_to_dict

os.environ['TESTING'] = 'true'

MODELS = [TimelinePost]

test_db = SqliteDatabase(':memory:')

class TestTimelinePost(unittest.TestCase):
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

    def test_timeline_post_creation(self):
        first_post = TimelinePost.create(name='John Doe', email='john@example.com', content="Hello world, I'm John!")
        self.assertEqual(first_post.id, 1)
        self.assertEqual(first_post.name, 'John Doe')
        self.assertEqual(first_post.email, 'john@example.com')
        self.assertEqual(first_post.content, "Hello world, I'm John!")

        second_post = TimelinePost.create(name='Jane Doe', email='jane@example.com', content="Hello world, I'm Jane!")
        self.assertEqual(second_post.id, 2)
        self.assertEqual(second_post.name, 'Jane Doe')
        self.assertEqual(second_post.email, 'jane@example.com')
        self.assertEqual(second_post.content, "Hello world, I'm Jane!")

    def test_get_timeline_posts(self):
        TimelinePost.create(name='John Doe', email='john@example.com', content="Hello world, I'm John!")
        TimelinePost.create(name='Jane Doe', email='jane@example.com', content="Hello world, I'm Jane!")

        posts = TimelinePost.select().order_by(TimelinePost.id)

        post_list = [model_to_dict(post, exclude=[TimelinePost.created_at]) for post in posts]

        expected_posts = [
            {'id': 1, 'name': 'John Doe', 'email': 'john@example.com', 'content': "Hello world, I'm John!"},
            {'id': 2, 'name': 'Jane Doe', 'email': 'jane@example.com', 'content': "Hello world, I'm Jane!"}
        ]

        self.assertEqual(post_list, expected_posts)

if __name__ == '__main__':
    unittest.main()