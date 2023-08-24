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
from django.utils.text import Truncator
from django.shortcuts import get_object_or_404

GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes"

api_key = config("API_KEY")


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
        user_profile = get_object_or_404(UserProfile, user=request.user)

        books_read = user_profile.books_read.all()
        books_want_to_read = user_profile.books_want_to_read.all()

        books_read_data = [{"id": book.id, "title": book.title} for book in books_read]
        books_want_to_read_data = [
            {"id": book.id, "title": book.title} for book in books_want_to_read
        ]

        data = {
            "username": user_profile.user.username,
            "books_read": books_read_data,
            "books_want_to_read": books_want_to_read_data,
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


# VIEW TO ADD A BOOK TO A USERS' WANT TO READ LIST
class AddToWantToReadView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, book_id):
        google_books_url = f"https://www.googleapis.com/books/v1/volumes/{book_id}"
        response = requests.get(google_books_url)
        if response.status_code != 200:
            return Response({"error": "Book not found in Google Books API"}, status=404)

        google_book_data = response.json()
        book_info = google_book_data.get("volumeInfo", {})
        print("Received Book Title:", book_info.get("title"))
        print("Author Length:", len(", ".join(book_info.get("authors", ["Unknown"]))))
        print(
            "Cover Image URL Length:",
            len(book_info.get("imageLinks", {}).get("thumbnail", "")),
        )
        print("Description Length:", len(book_info.get("description", "")))
        truncated_description = Truncator(book_info.get("description", "")).chars(190)
        book, created = Book.objects.get_or_create(
            external_id=book_id,
            defaults={
                "title": book_info.get("title", ""),
                "author": ", ".join(book_info.get("authors", ["Unknown"])),
                # "cover_image_url": book_info.get("imageLinks", {}).get("thumbnail", ""),
                "description": truncated_description,
            },
        )

        user_profile = request.user.userprofile
        user_profile.books_want_to_read.add(book)

        return Response({"message": "Book added to your 'want to read' list."})


# VIEW TO ADD A BOOK TO A USERS' READ LIST OR MOVE IT FROM WANT TO READ TO READ
class AddToReadView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, book_id):
        google_books_url = f"https://www.googleapis.com/books/v1/volumes/{book_id}"
        response = requests.get(google_books_url)
        if response.status_code != 200:
            return Response({"error": "Book not found in Google Books API"}, status=404)

        google_book_data = response.json()
        book_info = google_book_data.get("volumeInfo", {})
        truncated_description = Truncator(book_info.get("description", "")).chars(190)

        book_to_move, created = Book.objects.get_or_create(
            external_id=book_id,
            defaults={
                "title": book_info.get("title", ""),
                "author": ", ".join(book_info.get("authors", ["unknown"])),
                "description": truncated_description,
            },
        )

        user_profile = request.user.userprofile

        if book_to_move in user_profile.books_read.all():
            return Response({"message": "Book is already in your 'read' list."})

        user_profile.books_read.add(book_to_move)
        user_profile.books_want_to_read.remove(book_to_move)

        return Response(
            {"message": "Book marked as 'read' and moved to your 'read' list."}
        )


# DELETE A BOOK FROM USERS' WANT TO READ LIST
class DeleteWantToReadBook(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, pk):
        user_profile = UserProfile.objects.get(user=request.user)
        book_to_remove = get_object_or_404(Book, pk=pk)
        user_profile.books_want_to_read.remove(book_to_remove)

        return Response(
            {"message": f"Book {book_to_remove} removed from {user_profile}"}
        )


# DELETE A BOOK FROM USERS' READ LIST
class DeleteReadBook(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, pk):
        user_profile = UserProfile.objects.get(user=request.user)
        book_to_remove = get_object_or_404(Book, pk=pk)
        user_profile.books_read.remove(book_to_remove)

        return Response(
            {"message": f"{book_to_remove} removed from {user_profile}'s read list"}
        )
