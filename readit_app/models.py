from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission



class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=30)
    groups = models.ManyToManyField(
        Group,
        related_name="customuser_set",  # Add this related_name
        related_query_name="customuser",
        blank=True,
        help_text="The groups this user belongs to.",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_set",  # Add this related_name
        related_query_name="customuser",
        blank=True,
        help_text="Specific permissions for this user.",
    )


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    books_read = models.ManyToManyField(Book, related_name="read_by")
    books_want_to_read = models.ManyToManyField(Book, related_name="wanted_by")

    def __str__(self):
        return self.user.username


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    review_text = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"
