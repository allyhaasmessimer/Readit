from django.contrib import admin
from .models import User, Book, Review, UserProfile
from django.contrib.auth.admin import UserAdmin

admin.site.register(User, UserAdmin)
admin.site.register(Book)
admin.site.register(Review)
admin.site.register(UserProfile)
