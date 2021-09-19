import json
from rest_framework.test import APIRequestFactory, APITestCase
from django.urls import reverse


class BlogTestsSetup(APITestCase):
    """Setting up test variables"""

    def setUp(self, **kwargs):
        self.signup_url = reverse("api:users:signup")
        self.login_url = reverse("api:users:login")
        self.blog_posts_url = reverse("api:blog:blog-posts")
        self.blog_post_url = reverse("api:blog:blog-post")

        self.post_data = {
            "title": "Test blog post",
            "content": "This is just another blog post",
        }
        return super().setUp()

    def signup(self):
        self.client.post(
            self.signup_url,
            data={
                "email": "stam123@yopmail.com",
                "password1": "G00dpassword!",
                "password2": "G00dpassword!",
            },
            format="json",
        )

    def login(self):
        self.signup()
        login = self.client.post(
            self.login_url,
            data={"email": "stam123@yopmail.com", "password": "G00dpassword!"},
            format="json",
        )
        login_data = json.loads(login.content)
        jwt = login_data.get("user")["jwt"]["access"]
        return login, jwt


class BlogAPITests(BlogTestsSetup):
    """Blog tests"""

    def test_create_post_success(self):
        login, jwt = self.login()
        auth = self.client.credentials(HTTP_AUTHORIZATION="Bearer " + jwt)
        res = self.client.post(
            self.blog_post_url,
            data=self.post_data,
            format="json",
        )

        self.assertEqual(res.status_code, 201)

    def test_get_posts(self):
        login, jwt = self.login()
        auth = self.client.credentials(HTTP_AUTHORIZATION="Bearer " + jwt)
        create_post = self.client.post(
            self.blog_post_url,
            data=self.post_data,
            format="json",
        )

        res = self.client.get(self.blog_posts_url)
        posts = json.loads(res.content).get("posts")

        self.assertEqual(len(posts), 1)

    def test_like_unlike_post(self):
        from blog.models import BlogPost

        login, jwt = self.login()
        auth = self.client.credentials(HTTP_AUTHORIZATION="Bearer " + jwt)
        create_post = self.client.post(
            self.blog_post_url,
            data=self.post_data,
            format="json",
        )
        res = self.client.get(self.blog_posts_url)
        posts = json.loads(res.content).get("posts")
        post_id = posts[-1]["id"]
        blog_post = BlogPost.objects.get(id=post_id)

        blog_likes_url = reverse("api:blog:like", args=[1])
        res = self.client.post(blog_likes_url, data={"like": 1})
        self.assertEqual(blog_post.total_likes, 1)

        res = self.client.post(blog_likes_url, data={"like": 0})
        self.assertEqual(blog_post.total_likes, 0)
