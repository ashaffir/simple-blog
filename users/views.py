from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from users import serializers

from users.serializers import LoginSerializer, SignupSerializer, UserSerializer
from users.utils import EnrichUser


class SignupAPIView(GenericAPIView):
    """API endpoint for user signup"""

    permission_classes = [
        AllowAny,
    ]

    authentication_classes = []

    serializer_class = SignupSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = {}
        user = serializer.save(request)

        EnrichUser(user).start()

        data["user_id"] = user.id
        data["profile"] = serializer.data

        return Response({"user": data}, status=status.HTTP_201_CREATED)


class LoginAPIView(GenericAPIView):
    """API login view"""

    permission_classes = [
        AllowAny,
    ]

    authentication_classes = []

    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        user_data = {
            "id": user.pk,
            "username": user.username,
            "email": user.email,
            "jwt": user.tokens,
            "joined": str(user.joined),
        }

        return Response(
            {
                "user": user_data,
            },
            status=status.HTTP_200_OK,
        )


class UserProfile(GenericAPIView):
    """User data endpoint"""

    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request):
        try:
            serializer = self.serializer_class(request.user)
            return Response({"profile": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": e.args}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            user = request.user
            serializer = self.serializer_class(user, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {"success": "user profile updated"}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({"error": e.args}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            user = request.user
            user.delete()
            return Response(
                {"success": "user deleted"}, status=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            return Response({"error": e.args}, status=status.HTTP_400_BAD_REQUEST)
