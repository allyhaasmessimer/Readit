from django.test import TestCase
from .models import Book, CustomUser, UserProfile, Review

# class BasicTest(TestCase):
#     def test_basic(self):
#         self.assertEqual(1 + 1, 2)


class ModelTests(TestCase):
    def test_create_book(self):
        return Book.objects.create(author="jill", title="where the red fern grows")

    def test_create_custom_user(self):
        return CustomUser.objects.create(email="jill", username="wh", password="yuh")

    def test_create_user_profile(self):
        # Create a CustomUser instance
        user = CustomUser.objects.create(username="wh", password="yuh")
        # Create Book instances
        book_read = Book.objects.create(
            title="Where the Red Fern Grows", author="Author A"
        )
        book_want_to_read = Book.objects.create(title="The Bible", author="Author B")

        # Create UserProfile instance
        user_profile = UserProfile.objects.create(user=user)
        user_profile.books_read.add(book_read)
        user_profile.books_want_to_read.add(book_want_to_read)

        return user_profile

    def test_create_review(self):
        # Create a book instance
        book_1 = Book.objects.create(
            title="The Name of the Wind", author="Patrick Rothfus"
        )

        # Create a custom user instance
        user_1 = CustomUser.objects.create(username="allyhaas", password="yuh")

        # Create a review instance
        review = Review.objects.create(
            book=book_1, user=user_1, review_text="This was bad and not good"
        )

        # Assert that the review was created successfully
        self.assertEqual(review.book, book_1)
        self.assertEqual(review.user, user_1)
        self.assertEqual(review.review_text, "This was bad and not good")
        # Since date_posted is auto-generated, no need to check it explicitly

        # Optional: You can assert the count of Review objects in the database
        self.assertEqual(Review.objects.count(), 1)
