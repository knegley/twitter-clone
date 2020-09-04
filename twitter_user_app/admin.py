from django.contrib import admin
from twitter_user_app.models import TwitterUser
from django.contrib.auth.admin import UserAdmin

admin.site.register(TwitterUser, UserAdmin)
