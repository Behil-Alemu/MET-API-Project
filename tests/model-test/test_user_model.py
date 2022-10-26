
#    python -m unittest tests/model-test/test_user_model.py


import os
from unittest import TestCase
from sqlalchemy import exc
from psycopg2 import IntegrityError
from models import db, User, Post, Inspiration, Likes

os.environ['DATABASE_URL'] = "postgresql:///test_capstone_db"


from app import app

db.create_all()

class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Post.query.delete()
        Likes.query.delete()
        Inspiration.query.delete()
        db.session.commit()
        db.create_all()

        u1=User.signup(username='SamSMITH',      email='SamSMITH@gmail.com', avatar=None, password="Hashedpassword!"
        )
        u1_id=968747
        u1.id=u1_id

        u2=User.signup(username='Skip', email='Skip99@gmail.com', avatar=None, password="Hashedpassword!"
        )
        u2.id=986794

        db.session.commit()


        u1=User.query.get(u1.id)
        u2=User.query.get(u2.id)

        self.u1= u1
        self.u2= u2

        self.u1_id=u1.id
        self.u2_id=u2.id


        self.client = app.test_client()

    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        self.assertEqual(len(u.posts), 0)
        self.assertEqual(len(u.likes), 0)
        self.assertEqual(len(u.inspiration), 0)

    def test_repr(self):
        """id the __repr__ working properly"""
        repr(self.id)

    def test_user_signup(self):
        """check valid credentials place when signing up"""
        test_user= User.signup("username","useremail@gmail.com", "hashed_pwd", None)
        user_id= 93427
        test_user.id = user_id
        db.session.commit()

        user1 = User.query.get(user_id)
        self.assertEqual(user1.username, "username")
        self.assertEqual(user1.email, "useremail@gmail.com")
        self.assertNotEqual(user1.password, "hashed_pwd")
        self.assertNotEqual(user1.username, None)

    def test_invalid_pwds(self):
        """Test for invaild password"""
        with self.assertRaises(ValueError) as context:
            User.signup("username","useremail@gmail.com", "", None)
        with self.assertRaises(ValueError) as context:
            User.signup("username","useremail@gmail.com", None, None)

    def test_invalid_username(self):
        """test for invalid usernames"""
        test_user= User.signup(None,"useremail@gmail.com", "hashed_pwd", None)
        user_id= 93427
        test_user.id = user_id
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()


    def test_invalid_email(self):
        """check for invalid emails"""
        test_user= User.signup("Username",None, "hashed_pwd", None)
        user_id= 93427
        test_user.id = user_id
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_login(self):
        """Test authenticate"""
        user = User.authenticate(self.u1.username,'Hashedpassword!')
        self.assertIsNotNone(user)
        self.assertEqual(user.username, "SamSMITH")
        self.assertEqual(user.id, self.u1_id)
        self.assertEqual(user.password, self.u1.password)
        self.assertFalse(User.authenticate('NotUser', self.u1.password))
        self.assertTrue(User.authenticate(self.u1.username, "Hashedpassword!"))