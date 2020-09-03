from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth import login, logout, authenticate
from authentication.forms import LogInForm, Twitter_User_Signup, TweetForm
from authentication.models import TwitterUser, Tweet, Notification


def home_view(request):
    if not request.user.is_authenticated or request.user.is_anonymous:
        return HttpResponseRedirect(reverse("login"))
    tweets = [tweet for tweet in Tweet.objects.all()]
    notifications = Notification.objects.all()
    composed = TwitterUser.objects.get(
        username=request.user.username).tweet_set.all().count()
    followers = [follower.username for follower in TwitterUser.objects.get(
        id=request.user.id).followers.all()] or None

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
    print(request.path == "/signup/")
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


def tweet_view(request):
    form = TweetForm()
    if request.method == "POST":
        form = TweetForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # breakpoint()
            message = data.get("message")
            author = request.user
            Tweet.objects.create(message=message, author=author)
        return HttpResponseRedirect(reverse("home"))
    return render(request, "tweet.html", {"form": form})


def tweet_detailed_view(request, tweet_id):
    tweet = Tweet.objects.filter(id=tweet_id)
    # breakpoint()
    followers = [follower.username for follower in TwitterUser.objects.get(
        id=request.user.id).followers.all()] or None
    return render(request, "tweet_base.html", {"tweets": tweet, "followers": followers})


def follow_view(request, auth_id, tweet_id):
    """follows and unfollows the author for the user"""

    user = TwitterUser.objects.get(id=request.user.id)
    follower = TwitterUser.objects.get(id=auth_id)
    follower_username = follower.username
    followers = {follower for follower in TwitterUser.objects.get(
        id=request.user.id).followers.all()}

    if follower_username not in [f.username for f in followers]:
        followers.add(follower)
        # breakpoint()
        user.followers.set(followers)
    else:
        followers.remove(follower)
        user.followers.set(followers)

    # breakpoint()
    return HttpResponseRedirect(reverse("home"))
