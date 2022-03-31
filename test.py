from re import S
from unittest import TestCase

from app import app
from models import db, User, Post

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users_test_db'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


db.drop_all()
db.create_all()
 

class view_users_test(TestCase):
    """Test for views for users"""

    def setUp(self):
        """Add sample user"""
        Post.query.delete()
        User.query.delete()
          
        user = User(first_name="Test", last_name="User")
        db.session.add(user)
        db.session.commit()
        self.user_id = user.id

        post = Post(title="Test Post", content="Test Post!!", user_id=self.user_id)
        db.session.add(post)
        db.session.commit()            
        self.post_id = post.id
        

    def tearDown(self):
        """Clean up db"""

        db.session.rollback()

    def test_user_list(self):
        """Test if users list is shown"""
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test User', html)
        
    def test_user_details(self):
        """Test is user details are shown"""
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Test User</h1>', html)
   
    def test_edit_user(self):
        """Test if edit user page"""
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/edit")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Edit User: Test User', html)
    
    def test_add_user(self):
        """Test add user page"""
        with app.test_client() as client:
            resp = client.post(f"/users/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Add New User</h1>', html)
    

    def test_post(self):
        """Test post views"""
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Test Post</h1>', html)

    def test_post_on_user(self):
        """Test adding post"""
        with app.test_client() as client:
            resp = client.post(f"/users/{self.user_id}/posts/new", 
            data = {'title':'Test Post 2', 'content':'Test Post 2!!'},
            follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f"<h1>Test Post 2</h1>  ", html)
