from django.shortcuts import render, reverse, HttpResponseRedirect
from notification.models import Notification

# Create your views here.


def notification_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("home"))
    notification_tweets = [nt.tweet for nt in Notification.objects.filter(
        username_assigned_id=request.user.id) if not nt.has_read]

    notifications = [n.username_assigned.username for n in Notification.objects.filter(
        has_read=False)].count(request.user.username)

    notifications_to_change_status = Notification.objects.filter(
        username_assigned_id=request.user.id).filter(has_read=False)

    for notification in notifications_to_change_status:

        notification.has_read = True
        notification.save()

    return render(request, "notifications.html", {"tweets": notification_tweets, "notifications": notifications})
