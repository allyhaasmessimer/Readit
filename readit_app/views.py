from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User, UserProfile, Book
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
import os
import requests
from django.http import JsonResponse
from decouple import config

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
GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes"

api_key = config("API_KEY")


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


#   ADD USER PROFILE VIEW
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


# LIST OF FAV'D BOOKS BY A USER
class UserProfileListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user_profile = UserProfile.objects.get(user=request.user)

        books_read = [book.title for book in user_profile.books_read.all()]
        books_want_to_read = [
            book.title for book in user_profile.books_want_to_read.all()
        ]

        data = {
            "username": user_profile.user.username,
            "books_read": books_read,
            "books_want_to_read": books_want_to_read,
        }

        return Response(data)


# BOOK SEARCH
class SearchView(APIView):
    permission_classes = (AllowAny,)

    def book_search(self, value):
        param = {
            "q": value,
            "API_KEY": api_key,
        }
        api_url = "https://www.googleapis.com/books/v1/volumes"

        response = requests.get(url=api_url, params=param)
        data = response.json()
        print(data)
        return data.get("items", [])

    def post(self, request):
        search_query = request.data.get("q")

        if not search_query:
            return Response({"error": "Missing search query 'q'"}, status=400)

        search_results = self.book_search(search_query)
        return Response(search_results)
