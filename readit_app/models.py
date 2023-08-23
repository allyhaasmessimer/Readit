from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import Truncator


class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=150)

    def __str__(self):
        return self.username


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    cover_image_url = models.URLField()
    description = models.CharField(max_length=600)
    external_id = models.CharField(max_length=100, unique=False, default="", blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Truncate the description to 300 words
        self.description = Truncator(self.description).words(300, truncate=" ...")
        super().save(*args, **kwargs)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    books_read = models.ManyToManyField(Book, related_name="read_by", blank=True)
    books_want_to_read = models.ManyToManyField(
        Book, related_name="wanted_by", blank=True
    )

    def __str__(self):
        return self.user.username


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review_text = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"
