from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User, UserProfile, Book, Review
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


# GET USERNAME
class GetUsername(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        username = request.user.username
        return Response({"username": username})


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
                user_profile = UserProfile.objects.create(user=user)
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


# LOG OUT VIEW
class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        Token.objects.filter(user=user).delete()
        return Response({"message": "Logged out successfully."})


#   ADD USER PROFILE VIEW
# class AddUserProfile(APIView):
#     permission_classes = (IsAuthenticated,)

#     def post(self, request, *args, **kwargs):
#         user = request.user

#         books_read_titles = request.data.get("books_read")
#         books_want_to_read_titles = request.data.get("books_want_to_read")

#         user_profile, created = UserProfile.objects.get_or_create(user=user)

#         if books_read_titles:
#             books_read = Book.objects.filter(title__in=books_read_titles)
#             user_profile.books_read.add(*books_read)

#         if books_want_to_read_titles:
#             books_want_to_read = Book.objects.filter(
#                 title__in=books_want_to_read_titles
#             )
#             user_profile.books_want_to_read.add(*books_want_to_read)

#         user_profile.save()

#         return Response({"message": "User profile updated successfully."})


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

        if not books_read_data:
            books_read_data = []
        if not books_want_to_read_data:
            books_want_to_read_data = []

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

        full_url = f"{api_url}?q={param['q']}&API_KEY={param['API_KEY']}"
        print("Request URL:", full_url)

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

        truncated_description = Truncator(book_info.get("description", "")).chars(190)
        book, created = Book.objects.get_or_create(
            external_id=book_id,
            defaults={
                "title": book_info.get("title", ""),
                "author": ", ".join(book_info.get("authors", ["Unknown"])),
                "description": truncated_description,
            },
        )

        user_profile = request.user.userprofile
        print("User PROFILE:", user_profile)
        user_profile.books_want_to_read.add(book)
        print("Authenticated User:", request.user)

        return Response(
            {"message": f"Book added to your {user_profile} 'want to read' list."}
        )


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
        print("User PROFILE:", user_profile)
        print("Authenticated User:", request.user)

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
            {
                "message": f"Book {book_to_remove} removed from {user_profile} want to read list"
            }
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


# MAKE A REVIEW FOR A BOOK
class CreateReview(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        user = request.user
        book_to_review = get_object_or_404(Book, pk=pk)
        review_text = request.data.get("review_text")

        if user and book_to_review and review_text:
            new_review = Review.objects.create(
                user=user, book=book_to_review, review_text=review_text
            )
            new_review.save()
            return Response({"message": "Review created successfully."})
        else:
            return Response({"error": "Invalid data provided."}, status=400)


# GET ALL USERS' REVIEWS
class UserReviewsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        user_reviews = Review.objects.filter(user=user)

        reviews_data = []
        for review in user_reviews:
            review_data = {
                "id": review.id,
                "review_text": review.review_text,
                "date_posted": review.date_posted,
                "book_title": review.book.title,
            }
            reviews_data.append(review_data)

        return Response(reviews_data)


# DELETE REVIEW
class DeleteReview(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, pk):
        user = request.user
        review_to_delete = get_object_or_404(Review, pk=pk, user=user)
        review_to_delete.delete()

        return Response({"message": f"review removed from {user}'s review"})
