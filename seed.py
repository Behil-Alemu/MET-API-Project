"""Seed file to make sample data for db."""


from app import db
from models import User, Post, Likes, Inspiration
# Create all tables# DROP DATABASE capstone_db createdb capstone_db

db.drop_all() 
db.create_all()




# Add sample employees and departments
u1 = User(username='SamSMITH', email='SamSMITH@gmail.com', avatar='/static/images/default-pic.png', social_media="@SAM", bio="Love drawing and painting", password="Hashedpassword!")

u2 = User(username='Skip', email='Skip99@gmail.com', avatar='/static/images/default-pic.png', social_media="@Skippy", bio="Big fan of history", password="Hashedpassword!")

u3 = User(username='Raven_the_Bird', email='ravenray@gmail.com', avatar='/static/images/default-pic.png', social_media="@raven_bird", bio="Beginner to the art world", password="Hashedpassword!")

db.session.add_all([u1, u2, u3])
db.session.commit()
u1_post = Post(title='Sun rise', description="A painting of a sun rise in LA",  imageURL="https://tinyurl.com/demo-cupcake", created_at='09-10-2022', user_id=u1.id)

u3_post = Post(title='Liz', description="Drawing of my dear friend", imageURL="https://images.unsplash.com/photo-1569091791842-7cfb64e04797?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8NHx8ZHJhd2luZ3xlbnwwfHwwfHw%3D&auto=format&fit=crop&w=500&q=60", created_at='09-19-2022', user_id=u3.id)

db.session.add_all([ u1_post, u3_post])
db.session.commit()

L1=Likes(post_id=u1_post.id, user_id=u2.id)
L2=Likes(post_id=u1_post.id, user_id=u3.id)
L3=Likes(post_id=u3_post.id, user_id=u2.id)
L4=Likes(post_id=u3_post.id, user_id=u3.id)

Inspiration_1 =Inspiration(inspiration=976949, user_id=u1.id)
Inspiration_2 =Inspiration(inspiration=872389, user_id=u1.id)
Inspiration_3 =Inspiration(inspiration=423131, user_id=u2.id)


db.session.add_all([L1, L2, L3,L4, Inspiration_1, Inspiration_2, Inspiration_3])
db.session.commit()