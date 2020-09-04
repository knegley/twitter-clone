from django.urls import path
from twitter_user_app import views

urlpatterns = [
    path("follow/<int:auth_id>/", views.follow_view),
    path("profile/<str:author_name>/",
         views.twitter_user_profile_detailed, name="twitter_user_profile"),
    path("profile/", views.profile_view, name="profile"),
]
