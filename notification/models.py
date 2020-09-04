from django.db import models
from twitter_user_app.models import TwitterUser
from tweet.models import Tweet

# Create your models here.


class Notification(models.Model):
    has_read = models.BooleanField(default=False)

    username_assigned = models.ForeignKey(
        TwitterUser, on_delete=models.CASCADE, default=None)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.username_assigned.username
