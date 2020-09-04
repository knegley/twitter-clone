from django.urls import path
from authentication import views
urlpatterns = [
    path('', views.home_view, name="home"),
    path("follow/<int:auth_id>/", views.follow_view),
    #     path("tweet/<int:tweet_id>/profile/<str:author_name>/",
    #          views.twitter_user_profile_detailed),
    path("tweet/<int:tweet_id>/",
         views.tweet_detailed_view, name="detailed_tweet"),
    path("signup/", views.signup_view,
         name="signup"),
    path("login/", views.login_view, name="login"),
    path("profile/<str:author_name>/",
         views.twitter_user_profile_detailed, name="twitter_user_profile"),
    path("profile/", views.profile_view, name="profile"),
    path("tweet/", views.tweet_view, name="tweet"),
    path("notifications/", views.notification_view, name="notifications"),
    path("logout/", views.logout_view, name="logout")
]
