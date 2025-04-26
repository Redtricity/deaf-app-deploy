from .models import Notification

def unread_notifications_count(request):
    """
    Returns the number of unread notifications for the logged-in user.
    """
    # If no user is logged in
    if not request.user.is_authenticated:
        return {'unread_notifications_count': 0}

    # Count the notifications
    count = Notification.objects.filter(
        to_user=request.user,
        is_read=False
    ).count()

    return {'unread_notifications_count': count}
