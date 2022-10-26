    #  python -m unittest tests/model-test/test_like_model.py


import os
from unittest import TestCase

from models import db,  User, Post, Inspiration, Likes


os.environ['DATABASE_URL'] = "postgresql:///test_capstone_db"

from app import app

db.create_all()

class LikeModelTestCase(TestCase):
    """Test model for likes."""
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
    
    def test_post_likes(self): 
        """Test if message is in like"""
        p1 = Post(
            title="Happy",
            description="happy days",
            imageURL=None,
            user_id=self.u1.id
        )
        p2 = Post(
            title="sad",
            description="sad days",
            imageURL=None,
            user_id=self.u1.id
        )
        u2= User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )
        u2.id=9879
        

        db.session.add_all([p1,p2,u2])
        db.session.commit()

        u2.likes.append(p1)
        db.session.commit()
        self.assertIn(p1,u2.likes)
        self.assertIsInstance(p1.title, str)
        self.assertIsInstance(p2.description, str)
        self.assertEqual(len(u2.likes), 1)

        l = Likes.query.filter(Likes.user_id == u2.id).all()
        self.assertEqual(len(l), 1)
        self.assertEqual(l[0].post_id, p1.id)