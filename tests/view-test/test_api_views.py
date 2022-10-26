   
""" Inspiration View tests."""
#    Fpython -m unittest test_inspiration_views.py


import os
from unittest import TestCase
import requests

from requests import session

from models import db, connect_db, Post, User, Likes, Inspiration
from bs4 import BeautifulSoup


os.environ['DATABASE_URL'] = "postgresql:///test_capstone_db"


from app import app, CURR_USER_KEY



db.create_all()


app.config['WTF_CSRF_ENABLED'] = False

ObjectID = {
    "artistDisplayName": "Kiyohara Yukinobu",
    "primaryImage": "https://images.metmuseum.org/CRDImages/as/original/DP251139.jpg",
    "title": "Quail and Millet",
    "artistWikidata_URL": "https://www.wikidata.org/wiki/Q11560527"
}
    
class UserViewTestCase(TestCase):
    """Test views for user."""

    def setUp(self):
        """Create test client, add sample data."""

        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="hashed",
                                    avatar=None)
        self.testuser_id = 8989
        self.testuser.id = self.testuser_id

        self.u1 = User.signup("user1", "test1@test.com", "password1", None)
        self.u1_id = 778
        self.u1.id = self.u1_id

        self.u2 = User.signup("user2", "test2@test.com", "password2", None)
        self.u2_id = 884
        self.u2.id = self.u2_id


        db.session.commit()



    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback()  
    
    
    def setup_inspiration(self):
        I1 = Inspiration(id=998,inspiration=8705, user_id=self.testuser_id)
        I2 = Inspiration(inspiration=8955, user_id=self.testuser_id)
        I3 = Inspiration(inspiration=8945, user_id=self.u2_id)

        db.session.add_all([I1,I2,I3])
        db.session.commit()
   
   
    def test_users_saves(self):
        self.setup_inspiration()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id
            resp = c.get(f"/users/{self.testuser_id}/saves")
            self.assertEqual(resp.status_code, 200)

            I1 = Inspiration.query.filter(Inspiration.inspiration==8705).all()

    def test_list_homepage(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id
            resp = c.get("/")

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.content_type, "text/html; charset=utf-8")



    def test_get_objectID(self):
        # local host must be present
        self.maxDiff=None
        url = "https://127.0.0.1:5000/five-api"
        self.client.get("/")
        resp =requests.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 5)
        self.assertIn("primaryImage",str(resp.json()) )
        self.assertIn("artistDisplayName",str(resp.json()) )

 
                   

        
