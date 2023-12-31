from django.urls import path
from . import views


urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    # path("add_user_profile/", views.AddUserProfile.as_view(), name="add-user-profile"),
    path("list/", views.UserProfileListView.as_view(), name="list"),
    path("search/", views.SearchView.as_view(), name="search"),
    path(
        "want_to_read/<str:book_id>/",
        views.AddToWantToReadView.as_view(),
        name="add-to-want-to-read",
    ),
    path("read/<str:book_id>/", views.AddToReadView.as_view(), name="add-to-read"),
    path(
        "delete_want_to_read/<int:pk>/",
        views.DeleteWantToReadBook.as_view(),
        name="delete-want-to-read",
    ),
    path(
        "delete/<int:pk>/",
        views.DeleteReadBook.as_view(),
        name="delete-read",
    ),
    path("create_review/<int:pk>/", views.CreateReview.as_view(), name="create-review"),
    path("user/reviews/", views.UserReviewsView.as_view(), name="user-reviews"),
    path("delete_review/<int:pk>/", views.DeleteReview.as_view(), name="delete-review"),
    path("username/", views.GetUsername.as_view(), name="get-user")
]
