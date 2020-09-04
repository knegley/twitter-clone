from django.db import models
from django.utils import timezone
from twitter_user_app.models import TwitterUser
# Create your models here.


class Tweet(models.Model):
    time = models.DateTimeField(default=timezone.now)
    message = models.CharField(max_length=140)
    author = models.ForeignKey(TwitterUser, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-time"]

    def __str__(self):
        return self.message
