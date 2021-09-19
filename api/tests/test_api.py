from rest_framework.test import APIRequestFactory, APITestCase
from django.urls import reverse


class APITestsSetup(APITestCase):
    """Setting up test variables"""

    def setUp(self):
        self.signup_url = reverse("api:users:signup")
        self.login_url = reverse("api:users:login")

        return super().setUp()


class APITests(APITestsSetup):
    """API tests"""

    ################
    # TEST SIGNUP
    ################

    def test_signup_fail_email(self):
        res = self.client.post(
            self.signup_url,
            data={
                "email": "stam@mail",
                "password1": "G00dpassword!",
                "password2": "G00dpassword!",
            },
            format="json",
        )
        self.assertEqual(res.status_code, 400)

    def test_signup_fail_password_valid(self):
        res = self.client.post(
            self.signup_url,
            data={
                "email": "stam123@yopmail.com",
                "password1": "1234556",
                "password2": "1234556",
            },
            format="json",
        )
        print(f"{res.content=}")
        self.assertEqual(res.status_code, 400)

    def test_signup_fail_password_equal(self):
        res = self.client.post(
            self.signup_url,
            data={
                "email": "stam123@yopmail.com",
                "password1": "G00dpassword!",
                "password2": "G00dpassword!1",
            },
            format="json",
        )
        self.assertEqual(res.status_code, 400)

    def test_signup_success(self):
        res = self.client.post(
            self.signup_url,
            data={
                "email": "stam123@yopmail.com",
                "password1": "G00dpassword!",
                "password2": "G00dpassword!",
            },
            format="json",
        )
        self.assertEqual(res.status_code, 201)

    ################
    # TEST LOGIN
    ################

    def test_login_fail(self):
        self.test_signup_success()

        res = self.client.post(
            self.login_url,
            data={"email": "stam123@yopmail.com", "password": "wrongPassword"},
            format="json",
        )
        self.assertEqual(res.status_code, 403)

    def test_login_success(self):
        self.test_signup_success()

        res = self.client.post(
            self.login_url,
            data={"email": "stam123@yopmail.com", "password": "G00dpassword!"},
            format="json",
        )
        self.assertEqual(res.status_code, 200)
