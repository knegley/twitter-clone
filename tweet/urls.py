from django.urls import path
from tweet import views

urlpatterns = [
    path("tweet/<int:tweet_id>/",
         views.tweet_detailed_view, name="detailed_tweet"),
    path("tweet/", views.tweet_view, name="tweet"),
]
