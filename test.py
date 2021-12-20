from unittest import TestCase

from app import app
from models import db, Users, Posts

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UsersTest(TestCase):

    def setUp(self):
        Users.query.delete()
        Posts.query.delete()

        user = Users(first_name="F_Test", last_name="L_test", img_url="https://upload.wikimedia.org/wikipedia/commons/8/89/Portrait_Placeholder.png")
        post = Posts(title="Title_Test", content="Content")
        db.session.add(user, post)
        db.session.commit()

        self.user_id = user.id
        self.user = user
        self.post_id = post.id
        self.post = post

    def tearDown(self):
        db.session.rollback()


        """
        def test_index_load(self):
        with app.test_client() as client:
            res = client.get("/")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('Users', html) """


    def test_user_detail_page(self):
        with app.test_client() as client:
            res = client.get(f"/{self.user_id}")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn(self.user.first_name, html)
            self.assertIn(self.user.last_name, html)

        
        """
        def test_add_user(self):
        with app.test_client() as client:
            test_user = {"first_name": "Mad", "last_name": "Max", "image":"https://upload.wikimedia.org/wikipedia/commons/8/89/Portrait_Placeholder.png"}
            res = client.user("/adduser", data=test_user, follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Mad Max", html)
        """


    def test_user_id_query_url(self):
        with app.test_client() as client:
            res = client.get(f"/123456789")

            self.assertEqual(res.status_code, 404)


    def test_post_detail_page(self):
        with app.test_client() as client:
            res = client.get(f"/{self.post_id}")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn(self.post.title, html)
            self.assertIn(self.post.content, html)


    def test_add_post(self):
        with app.test_client() as client:
            test_post = {"title": "Here is a title", "content": "Some content", "creator_id": 1}
            res = client.post("/addpost", data=test_post, follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Here is a title", html)


    def test_post_id_query_url(self):
        with app.test_client() as client:
            res = client.get(f"/post/0")

            self.assertEqual(res.status_code, 200)


