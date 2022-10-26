    #  python -m unittest tests/model-test/test_inspiration_model.py


import os
from unittest import TestCase

from models import db,  User, Post, Inspiration, Likes


os.environ['DATABASE_URL'] = "postgresql:///test_capstone_db"

from app import app

db.create_all()

class InspirationModelTestCase(TestCase):
    """Test model for inspiration."""
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
    
    def test_art_inspiration(self): 
        """Test if message is in like"""
        art1 = Inspiration(
            inspiration=8753,
            user_id=self.u1.id
        )
        art2 = Inspiration(
            inspiration=8054,
            user_id=self.u1.id
        )
        

        db.session.add_all([art1,art2])
        db.session.commit()

        I = Inspiration.query.filter(Inspiration.user_id ==  self.u1.id).all()
        self.assertIn(art1,self.u1.inspiration)
        self.assertIn(art2,self.u1.inspiration)
        self.assertIsInstance(art1.inspiration, int)
        self.assertEqual(len(I), 2)
        self.assertEqual(I[0].user_id, self.u1.id)
        self.assertEqual(art1.user_id, self.u1.id)
        self.assertEqual(len(self.u1.inspiration), 2)

