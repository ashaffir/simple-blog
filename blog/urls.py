from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("blog-posts/", views.BlogPostsView.as_view(), name="blog-posts"),
    path("blog-post/", views.SinglePostView.as_view(), name="blog-post"),
    path("like/<int:id>/", views.LikeAPIView.as_view(), name="like"),
]
