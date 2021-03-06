from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth import login, logout, authenticate
from authentication.forms import LogInForm, Twitter_User_Signup
from twitter_user_app.models import TwitterUser
from tweet.models import Tweet
from notification.models import Notification


def home_view(request):
    if not request.user.is_authenticated or request.user.is_anonymous:
        return HttpResponseRedirect(reverse("login"))

    notifications = [n.username_assigned.username for n in Notification.objects.filter(
        has_read=False)].count(request.user.username)

    composed = TwitterUser.objects.get(
        username=request.user.username).tweet_set.all().count()

    if composed is not None:
        followers = [follower.username for follower in TwitterUser.objects.get(
            id=request.user.id).followers.all()] or ""
        tweets = [tweet for tweet in Tweet.objects.all()
                  if tweet.author.username in followers or tweet.author.username == request.user.username]

    return render(request, "home.html", {"notifications": notifications,
                                         "tweets": tweets,
                                         "composed": composed,
                                         "followers": followers})


def login_view(request):
    form = LogInForm()
    if request.method == "POST":
        form = LogInForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data.get("username")
            password = data.get("password")
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("home"))
    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def signup_view(request):
    form = Twitter_User_Signup()

    if request.method == "POST":
        form = Twitter_User_Signup(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            username = data.get("username")
            password = data.get("password")
            first_name = data.get("first_name")
            last_name = data.get("last_name")

            TwitterUser.objects.create_user(
                username=username,
                password=password, first_name=first_name, last_name=last_name
            )
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("home"))

    return render(request, "signup.html", {"form": form})
