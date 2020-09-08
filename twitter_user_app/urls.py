from django.urls import path
from twitter_user_app import views

urlpatterns = [
    path("follow/<int:auth_id>/", views.FollowView.as_view()),
    path("profile/<str:author_name>/",
         views.TwitterUserProfileDetailed.as_view(), name="twitter_user_profile"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
]
