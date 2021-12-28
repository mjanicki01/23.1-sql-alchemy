from unittest import TestCase

from app import app
from models import db, Users, Posts, Tags, PostsTags

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_testdb'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BloglyTest(TestCase):

    def setUp(self):
#reset DB from seed.py
        self.users = Users
        self.tags = Tags
        self.posts = Posts
        self.poststags = PostsTags

    def tearDown(self):
        db.session.rollback()


    def test_index_load(self):
        with app.test_client() as client:
            res = client.get("/")
            html = res.get_data(as_text=True)

        self.assertEqual(res.status_code, 200)
        self.assertIn('Users', html)


    def test_user_detail_page(self):
        with app.test_client() as client:   
            test_user = Users.query.get_or_404(2)
            res = client.get("/2")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn(test_user.first_name, html)
            self.assertIn(test_user.last_name, html)


    def test_add_user(self):
        with app.test_client() as client:
            test_user = {"first_name": "Mad", "last_name": "Max", "image":"https://upload.wikimedia.org/wikipedia/commons/8/89/Portrait_Placeholder.png"}
            res = client.post("/adduser", data=test_user, follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Mad Max", html)


    def test_delete_user(self):
        with app.test_client() as client:
            test_user = Users.query.filter_by(first_name='Mad').first()
            test_user_id = test_user.id
            res = client.post(f"/delete/<int:{test_user_id}>", data=test_user_id, follow_redirects=True) #AttributeError: 'int' object has no attribute 'items'
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertNotIn("Mad Max", html)


    def test_user_id_query_url(self):
        with app.test_client() as client:
            res = client.get(f"/123456789")

            self.assertEqual(res.status_code, 404)

   
    def test_post_detail_page(self):
        with app.test_client() as client:
            test_post = Posts.query.get_or_404(1)
            res = client.get("/post/1")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn(test_post.title, html)
            self.assertIn(test_post.content, html)
    
    """
    def test_add_post(self):
        with app.test_client() as client:
            test_post = {"title": "Here is a title", "content": "Some content", "creator_id": 1}
            res = client.posts("/addpost", data=test_post, follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Here is a title", html)
    """

    def test_post_id_query_url(self):
        with app.test_client() as client:
            res = client.get(f"/post/1")

            self.assertEqual(res.status_code, 200)


