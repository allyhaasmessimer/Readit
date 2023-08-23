from django.urls import path
from . import views


urlpatterns = [
    path("hello/", views.HelloView.as_view(), name="hello"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("login/", views.LoginView.as_view(), name="login"),
    path('add_user_profile/', views.AddUserProfile.as_view(), name='add-user-profile'),
    path('list/', views.UserProfileListView.as_view(), name="list"),
    path('search/', views.SearchView.as_view(), name='search'),
    path('want_to_read/<str:book_id>/', views.AddToWantToReadView.as_view(), name='add-to-want-to-read'),
    path('read/<str:book_id>/', views.AddToReadView.as_view(), name='add-to-want-to-read'),

]
