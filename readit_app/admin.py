from django.contrib import admin
from .models import CustomUser, Book, UserProfile, Review

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    pass

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    pass

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    pass

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass
