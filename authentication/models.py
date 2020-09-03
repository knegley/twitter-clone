from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class TwitterUser(AbstractUser):
    followers = models.ManyToManyField("self", symmetrical=False)

    def __str__(self):
        return self.username


class Tweet(models.Model):
    time = models.DateTimeField(default=timezone.now)
    message = models.CharField(max_length=140)
    author = models.ForeignKey(TwitterUser, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-time"]

    def __str__(self):
        return self.message


class Notification(models.Model):
    has_read = models.BooleanField(default=False)
    # tweet = models.ManyToManyField(Tweet,on_delete=models.CASCADE)
    # username_assigned=models.CharField(max_length=20)
    username_assigned = models.ForeignKey(
        TwitterUser, on_delete=models.CASCADE, default=None)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, default=None)

    # count = models.IntegerField(default=0)

    # def increment(self):
    #     return self.count+1

    # def decrement(self):
    #     return self.count-1

    # def __str__(self):
    #     return self.count
