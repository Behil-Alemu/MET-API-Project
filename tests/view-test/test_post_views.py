"""post View tests."""

#    python -m unittest test_post_views.py


import os
from unittest import TestCase

from requests import post

from models import Likes, db, connect_db, Post, User,Inspiration
from flask import session



os.environ['DATABASE_URL'] = "postgresql:///test_capstone_db"



from app import app, CURR_USER_KEY


db.create_all()


app.config['WTF_CSRF_ENABLED'] = False


class PostViewTestCase(TestCase):
    """Test views for post."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Post.query.delete()
        Likes.query.delete()
        Inspiration.query.delete()
        db.session.commit()
        db.create_all()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    avatar=None)
        self.testuser_id = 8989
        self.testuser.id = self.testuser_id             

        db.session.commit()
    def tearDown(self):
        """Clean up fouled transactions."""
        db.session.rollback()

    def test_add_post(self):
        """Can use add a post?"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

      

            resp = c.post("/post/new", data={"title": "sad", "description":"sad art", "imageURL":"https://tinyurl.com/demo-cupcake"})

            # Make sure it redirects
            self.assertEqual(resp.status_code, 302)

            post = Post.query.one()
            self.assertEqual(post.title, "sad")
            self.assertEqual(post.description, "sad art")

    def test_add_no_session(self):
        """adding post without loging in will not be authorized"""
        with self.client as c:
            resp = c.post("/post/new", data={"title": "sad", "description":"sad art", "imageURL":"https://tinyurl.com/demo-cupcake"}, follow_redirects=True )
           
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn(CURR_USER_KEY, session)
            self.assertIn(b'Please sign up first : }', resp.data)

    def test_add_invalid_user(self):
        """no access for invalid users"""


        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = 878876


            resp = c.post("/post/new", data={"title": "sad", "description":"sad art", "imageURL":"https://tinyurl.com/demo-cupcake"}, follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(CURR_USER_KEY, session)
            self.assertIn('Please sign up first : }', resp.data)

    
    def test_post_show(self):
        """show  list of <int:post_id>"""
        
        p= Post(
            id= 939,
            title= "sad",
            description="sad art",
            imageURL="https://tinyurl.com/demo-cupcake",
            user_id=self.testuser_id )

        db.session.add(p)
        db.session.commit()

       
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            p= Post.query.get(939)

            resp= c.get(f"/post/{p.id}/edit")
            self.assertEqual(resp.status_code, 200)
            self.assertIn(p.title, str(resp.data))

    def test_edit_invalid_user(self):
        """no access for invalid post id"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp= c.post('/post/986297/edit')
            self.assertNotEqual(resp.status_code, 200)

    def test_edit_valid_user(self):
        """ access for valid post id"""
        p= Post(
            id= 939,
            title= "sad",
            description="sad art",
            imageURL="https://tinyurl.com/demo-cupcake",
            user_id=self.testuser_id )

        db.session.add(p)
        db.session.commit()
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp= c.post(f'/post/{p.id}/edit')
            self.assertNotEqual(resp.status_code, 200)

    def test_message_delete(self):
        """DElect message working properly"""
        p= Post(
            id= 939,
            title= "sad",
            description="sad art",
            imageURL="https://tinyurl.com/demo-cupcake",
            user_id=self.testuser_id )

        db.session.add(p)
        db.session.commit()

       
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            p= Post.query.get(939)
            resp= c.post(f"/post/{p.id}/delete")
            self.assertEqual(resp.status_code, 302)
            self.assertNotIn(p.title, str(resp.data))

    def test_add_invalid_post(self):
        """no delete access for invalid message id"""
        p= Post(
            id= 939,
            title= "sad",
            description="sad art",
            imageURL="https://tinyurl.com/demo-cupcake",
            user_id=self.testuser_id )

        db.session.add(p)
        db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] =self.testuser.id

            resp= c.get('/post/7858/delete')
            self.assertNotEqual(resp.status_code, 200)
            



