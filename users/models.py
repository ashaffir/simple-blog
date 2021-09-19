from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import BlacklistMixin, RefreshToken


class User(AbstractUser):
    """User DB model.
    This is the 'root' user that used for the registration of new users.
    """

    username = models.CharField(max_length=200, blank=False)
    email = models.EmailField(max_length=200, unique=True, blank=False)
    joined = models.DateTimeField(auto_now_add=True)
    ip_address = models.CharField(max_length=15, null=True, blank=True)
    holiday = models.JSONField(null=True, blank=True, default=dict)
    # require the email to be the unique identifier
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
    ]

    def __str__(self):
        return self.email

    @property
    def tokens(self):
        """Create a JWT & refresh tokens for a user"""
        refresh = RefreshToken.for_user(self)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}
