from django.shortcuts import render, HttpResponseRedirect, reverse
from tweet.models import Tweet
from notification.models import Notification
from twitter_user_app.models import TwitterUser
from django.views.generic import TemplateView


class TwitterUserProfileDetailed(TemplateView):

    def get(self, request, author_name):
        try:
            TwitterUser.objects.get(username=author_name)
        except Exception:
            return HttpResponseRedirect(reverse("home"))

        composed = TwitterUser.objects.get(
            username=author_name).tweet_set.all().count()
        followers = [follower.username for follower in TwitterUser.objects.get(
            username=author_name).followers.all()]
        tweets = [tweet for tweet in Tweet.objects.all()
                  if tweet.author.username == author_name]
        return render(request, "profile.html", {
            "tweets": tweets,
            "composed": composed,
            "followers": ", ".join(followers) or None,
            "author_name": author_name,
            "f": len(followers) or 0
        })


class FollowView(TemplateView):

    def get(self, request, auth_id):
        """follows and unfollows the author for the user"""
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("home"))

        try:
            TwitterUser.objects.get(id=auth_id)
        except Exception:

            return HttpResponseRedirect(reverse("home"))

        if TwitterUser.objects.get(id=auth_id) == request.user:
            return HttpResponseRedirect(reverse("home"))

        user = TwitterUser.objects.get(id=request.user.id)
        follower = TwitterUser.objects.get(id=auth_id)
        follower_username = follower.username
        followers = {follower for follower in TwitterUser.objects.get(
            id=request.user.id).followers.all()}

        if follower_username not in [f.username for f in followers]:
            followers.add(follower)

            user.followers.set(followers)
        else:
            followers.remove(follower)
            user.followers.set(followers)

        return HttpResponseRedirect(reverse("home"))


class ProfileView(TemplateView):

    def get(self, request):
        if request.user.is_anonymous:
            return HttpResponseRedirect(reverse("home"))

        notifications = [n.username_assigned.username for n in Notification.objects.filter(
            has_read=False)].count(request.user.username)

        composed = TwitterUser.objects.get(
            username=request.user.username).tweet_set.all().count()
        if composed is not None:
            followers = ", ".join([follower.username for follower in TwitterUser.objects.get(
                id=request.user.id).followers.all()])
            tweets = [tweet for tweet in Tweet.objects.all()
                      if tweet.author.username == request.user.username]

        return render(request, "profile.html", {"notifications": notifications,
                                                "tweets": tweets,
                                                "composed": composed,
                                                "followers": followers or None,
                                                "f": len(followers.split()) or 0})
