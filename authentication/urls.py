from django.urls import path
from authentication import views
urlpatterns = [
    path('', views.home_view, name="home"),
    path("tweet/<int:tweet_id>/",
         views.tweet_detailed_view, name="detailed_tweet"),
    path("follow/<int:auth_id>/", views.follow_view),
    path("signup/", views.signup_view,
         name="signup"),
    path("login/", views.login_view, name="login"),
    path("tweet/", views.tweet_view, name="tweet"),
    path("logout/", views.logout_view, name="logout")
]
