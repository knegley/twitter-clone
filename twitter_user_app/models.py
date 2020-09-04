from django.db import models
from django.contrib.auth.models import AbstractUser


class TwitterUser(AbstractUser):
    followers = models.ManyToManyField("self", symmetrical=False)

    def __str__(self):
        return self.username
