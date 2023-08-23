from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User, UserProfile, Book
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated


# from django.contrib.auth.models import User
# from rest_framework.authtoken.views import ObtainAuthToken
# import requests
# from django.http import JsonResponse
# from django.views import View
# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.permissions import AllowAny
# from .models import CustomUser, UserProfile, Book, Review
# from rest_framework.generics import RetrieveAPIView
# from django.shortcuts import get_object_or_404

# GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes"


# protected view
class HelloView(APIView):
    #     permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {"message": "Hello, World!"}
        return Response(content)


#  SIGN UP VIEW
class SignUpView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")

        if username and password and email:
            user, created = User.objects.get_or_create(username=username, email=email)
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


#   LOG IN VIEW
class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({"token": token.key})
            else:
                return Response({"error": "Invalid credentials"}, status=400)
        else:
            return Response(
                {"error": "Both username and password are required."}, status=400
            )


class AddUserProfile(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user

        books_read_titles = request.data.get("books_read")
        books_want_to_read_titles = request.data.get("books_want_to_read")

        user_profile, created = UserProfile.objects.get_or_create(user=user)

        if books_read_titles:
            books_read = Book.objects.filter(title__in=books_read_titles)
            user_profile.books_read.add(*books_read)

        if books_want_to_read_titles:
            books_want_to_read = Book.objects.filter(
                title__in=books_want_to_read_titles
            )
            user_profile.books_want_to_read.add(*books_want_to_read)

        user_profile.save()

        return Response({"message": "User profile updated successfully."})


#         custom_users = CustomUser.objects.all()
#         data = {
#             "username": list(custom_users.values())
#         }
#         return Response(data)

# username = request.query_params.get('username')
# print("USERNAME", username)
# user = CustomUser.objects.get(username=username)
# user_profile = UserProfile.objects.get(user=user)

# data = {
#     "books_read": list(user_profile.books_read.values()),  # Convert to list
#     "books_want_to_read": list(
#         user_profile.books_want_to_read.values()
#     ),  # Convert to list
# }
# return Response(data)
