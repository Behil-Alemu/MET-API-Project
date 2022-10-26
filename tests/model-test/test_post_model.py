#  python -m unittest tests/model-test/test_post_model.py


import os
from unittest import TestCase

from models import db,  User, Post, Inspiration, Likes


os.environ['DATABASE_URL'] = "postgresql:///test_capstone_db"

from app import app

db.create_all()

class PostModelTestCase(TestCase):
    """Test views for messages."""
    def setUp(self):
        """Create test client, add sample data."""
        User.query.delete()
        Post.query.delete()
        Likes.query.delete()
        Inspiration.query.delete()
        db.session.commit()
        db.create_all()

        u1=User.signup(username="user1",
            email="email1@gmail.com",
            password="hashed_pwd",
            avatar=None
        )
    
        self.u1_id=968747
        u1.id=self.u1_id

        u1=User.query.get(self.u1_id)

        self.u1= u1
        

        self.client = app.test_client()

    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback()
    
    def test_post_model(self):
        """Does basic model work?"""

        m = Post(
            title="Happy",
            description="happy days",
            imageURL=None,
            user_id=self.u1.id,
        )

        db.session.add(m)
        db.session.commit()

        self.assertEqual(len(m.title), 5)
        self.assertEqual(len(m.description), 10)
        self.assertEqual(len(self.u1.posts), 1)
        self.assertEqual(m.title, "Happy")
        self.assertEqual(m.description, "happy days")

    def test_post_friendly_date(self):
        """Does friendly_date property work?"""

        m = Post(
            title="Happy",
            description="happy days",
            imageURL=None,
            user_id=self.u1.id,
            created_at= "1990-08-01 09:34:10"
        )
        db.session.add(m)
        db.session.commit()

        self.assertTrue("1990-08-01 09:34:10")
        self.assertEqual(m.friendly_date,"Wed Aug 1 1990, 9:34 AM")
        self.assertNotEqual(m.friendly_date,"1990-08-01 09:34:10")
