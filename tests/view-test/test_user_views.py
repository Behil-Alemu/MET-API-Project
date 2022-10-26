"""User View tests."""
#     python -m unittest test_message_views.py


import os
from unittest import TestCase

from requests import session

from models import db, connect_db, Post, User, Likes, Inspiration
from bs4 import BeautifulSoup


os.environ['DATABASE_URL'] = "postgresql:///test_capstone_db"


from app import app, CURR_USER_KEY



db.create_all()


app.config['WTF_CSRF_ENABLED'] = False


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


    def test_user_show(self):
        with self.client as c:
            resp = c.get(f"/user/{self.testuser_id}/profile")

            self.assertEqual(resp.status_code, 200)
            self.assertIn("testuser", str(resp.data))

    def setup_likes(self):
        p1 = Post(
            title="Happy",
            description="happy days",
            imageURL=None,
            user_id=self.u1_id
        )
        p2 = Post(id=976,
            title="sad",
            description="sad days",
            imageURL=None,
            user_id=self.u1_id
        )
        p3 = Post(
            title="silly",
            description="silly days",
            imageURL=None,
            user_id=self.testuser_id
        )
        

        db.session.add_all([p1,p2,p3])
        db.session.commit()

        l1 = Likes(user_id=self.testuser_id, post_id=976)
        db.session.add(l1)
        db.session.commit()

    def test_user_show_info(self):
        self.setup_likes()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id

            resp = c.get(f"/users/{self.testuser_id}")
            self.assertEqual(resp.status_code, 200)

            self.assertIn('testuser', str(resp.data))
            soup = BeautifulSoup(str(resp.data), 'html.parser')
            found = soup.find_all("li", {"class": "stat"})
            self.assertEqual(len(found), 1)

            # test for a count of 1 messages
            self.assertIn("1", found[0].text)



    def test_add_like(self):
        p1 = Post(id=194,
            title="Happy",
            description="happy days",
            imageURL=None,
            user_id=self.u1_id
        )
        db.session.add(p1)
        db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id

            resp = c.post("/posts/194/like", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)

            likes = Likes.query.filter(Likes.post_id==194).all()
            self.assertEqual(len(likes), 1)
            self.assertEqual(likes[0].user_id, self.testuser_id)

    def test_show_likes(self):
        p1 = Post(id=194,
            title="Happy",
            description="happy days",
            imageURL=None,
            user_id=self.testuser_id
        )
        db.session.add(p1)
        db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id

            resp = c.get(f"/users/{self.testuser_id}/likes")
            self.assertEqual(resp.status_code, 200)

            likes = Likes.query.filter(Likes.post_id==194).all()
            self.assertEqual(len(likes), 0)
     

    def test_toggle_like(self):
        self.setup_likes()

        p = Post.query.filter(Post.title=="sad").one()
        self.assertIsNotNone(p)
        self.assertNotEqual(p.user_id, self.testuser_id)

        l = Likes.query.filter(
            Likes.user_id==self.testuser_id and Likes.post_id==p.id
        ).one()

        self.assertIsNotNone(l)

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id

            resp = c.post(f"/posts/{p.id}/like", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)

            likes = Likes.query.filter(Likes.post_id==p.id).all()
            # when button clicked again the like has been deleted
            self.assertEqual(len(likes), 0)

    def test_unauthenticated_like(self):
        self.setup_likes()

        p = Post.query.filter(Post.title=="sad").one()
        self.assertIsNotNone(p)

        like_count = Likes.query.count()

        with self.client as c:
            resp = c.post(f"/posts/{p.id}/like", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)

            self.assertIn("Access unauthorized", str(resp.data))

            # The number of likes has not changed since making the request
            self.assertEqual(like_count, Likes.query.count())

    def test_user_delete(self):
        """DElect user profile in route """
      
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            u1= User.query.get(self.testuser.id)
            resp= c.post(f"/users/{self.testuser.id}/delete")
            self.assertEqual(resp.status_code, 302)
            self.assertNotIn(u1.username, str(resp.data))


    def test_valid_edit_user(self): 
        """ access edit for valid user id"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            u1= User.query.get(self.testuser.id)
            resp= c.post(f'users/profile')
            self.assertEqual(resp.status_code, 200)
            self.assertIn(u1.username, str(resp.data))

   

