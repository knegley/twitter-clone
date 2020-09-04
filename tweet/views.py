from django.shortcuts import render, HttpResponseRedirect, reverse
from tweet.forms import TweetForm
from tweet.models import Tweet
from notification.models import Notification
from twitter_user_app.models import TwitterUser
# Create your views here.


def tweet_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))

    form = TweetForm()
    usernames = [user.username for user in TwitterUser.objects.all()]
    if request.method == "POST":
        form = TweetForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            message = data.get("message")

            word_list = message.split()
            users = {w for word in word_list if word.startswith(
                "@") and (w := word[1:]) in usernames and w != request.user.username}

            author = request.user
            if users:
                tweet = Tweet.objects.create(message=message, author=author)
                for user in users:
                    assigned_user = TwitterUser.objects.get(username=user)
                    Notification.objects.create(
                        username_assigned=assigned_user, tweet=tweet)
            else:
                Tweet.objects.create(message=message, author=author)

        return HttpResponseRedirect(reverse("home"))
    return render(request, "tweet.html", {"form": form})


def tweet_detailed_view(request, tweet_id):

    try:
        Tweet.objects.get(id=tweet_id)
    except Exception:
        return HttpResponseRedirect(reverse("home"))

    tweet = Tweet.objects.filter(id=tweet_id)
    is_following = "unfollow "
    followers = None

    if request.user.is_authenticated:
        followers = [follower.username for follower in TwitterUser.objects.get(
            id=request.user.id).followers.all()]

    if followers is not None and tweet.first().author.username not in followers:
        is_following = "follow "

    return render(request, "tweet_base.html", {"tweets": tweet, "is_following": is_following})
