from django.core.exceptions import ObjectDoesNotExist
from django.db import reset_queries
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import serializers, status

from .serializers import BlogPostSerializer, PostLikeSerializer
from .models import BlogPost


class BlogPostsView(GenericAPIView):
    """API poing for getting the list of all blog posts"""

    permission_classes = [AllowAny]
    serializer_class = BlogPostSerializer

    def get(self, request):
        serializer = self.serializer_class(BlogPost.objects.all(), many=True)
        return Response({"posts": serializer.data}, status=status.HTTP_200_OK)


class SinglePostView(GenericAPIView):
    """Single post operations"""

    permission_classes = [IsAuthenticated]
    serializer_class = BlogPostSerializer

    def post(self, request):
        """Create a simgle blog post"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            BlogPost.objects.create(
                title=serializer.validated_data["title"],
                content=serializer.validated_data["content"],
                author=request.user,
            )
            return Response(
                {"success": "blog post created"}, status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response({"error": e.args}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        """Update blog post"""
        from users.models import User

        try:
            post_id = request.data["post_id"]
            blog_post = BlogPost.objects.get(id=post_id)
            if request.user == blog_post.author:
                serializer = self.serializer_class(blog_post, data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(
                    {"success": "blog post updated"}, status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"error": "update action not authorized"},
                    status=status.HTTP_403_FORBIDDEN,
                )
        except Exception as e:
            return Response({"error": e.args}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """Delete a blog post"""
        try:
            post_id = request.data["post_id"]
            blog_post = BlogPost.objects.get(id=post_id)
            if request.user == blog_post.author:
                blog_post.delete()
                return Response(
                    {"success": "blog post deleted"}, status=status.HTTP_204_NO_CONTENT
                )
            else:
                return Response(
                    {"error": "delete action not authorized"},
                    status=status.HTTP_403_FORBIDDEN,
                )
        except Exception as e:
            return Response({"error": e.args}, status=status.HTTP_400_BAD_REQUEST)


class LikeAPIView(GenericAPIView):
    """Blog post like API endpoint to receive likes and un-likes.
    - Post ID should be retrieved from the blog-posts GET request that lists all posts.
    - like = 1 => 'like' and other value with be to unlike
    """

    permission_classes = [IsAuthenticated]
    serializer_class = PostLikeSerializer

    def post(self, request, id):
        try:
            blog_post = BlogPost.objects.get(id=id)
            if int(request.data["like"]) == 1:
                blog_post.likes.add(request.user)
            else:
                blog_post.likes.remove(request.user)

            post_likes = blog_post.total_likes
            return Response(
                {
                    "success": f"user {request.user} likes post {id}. Total likes: {post_likes}"
                },
                status=status.HTTP_200_OK,
            )
        except ObjectDoesNotExist as e:
            return Response({"error": e.args}, status=status.HTTP_404_NOT_FOUND)
