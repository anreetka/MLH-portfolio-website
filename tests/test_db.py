import unittest
from peewee import SqliteDatabase
from app import TimelinePost

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
