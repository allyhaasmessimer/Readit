from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken


# protected view
class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {"message": "Hello, World!"}
        return Response(content)


# sign up view
class SignUpView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if username and password:
            user, created = User.objects.get_or_create(username=username)
            if created:
                user.set_password(password)
                user.save()
                token, token_created = Token.objects.get_or_create(user=user)
                return Response({"token": token.key})
            else:
                return Response({"error": "Username already exists."}, status=400)
        else:
            return Response(
                {"error": "Both username and password are required."}, status=400
            )


# log in view
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = response.data.get("token")
        if token:
            return Response({"token": token})
        return Response({"error": "Invalid credentials"}, status=400)
