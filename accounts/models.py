from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField

# Create your models here.

class IdentityTag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Profile(models.Model):
    HEARING_STATUS_CHOICES = [
        ('deaf', 'Deaf'),
        ('hard_of_hearing', 'Hard of Hearing'),
        ('hearing', 'Hearing'),
        ('prefer_not_to_say', 'Prefer not to say'),
    ]

    SIGN_LANGUAGE_CHOICES = [
        ('bsl', 'British Sign Language'),
        ('asl', 'American Sign Language'),
        ('other', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    location = CountryField(blank_label='(Select country)', null=True, blank=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    is_public = models.BooleanField(default=True)
    hearing_status = models.CharField(max_length=20, choices=HEARING_STATUS_CHOICES, default='prefer_not_to_say')
    sign_language_preference = models.CharField(max_length=10, choices=SIGN_LANGUAGE_CHOICES, default='bsl')
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='profile_pictures/default_user.jpg', blank=True)

    identity_tags = models.ManyToManyField(IdentityTag, blank=True)

    
class Follow(models.Model):
    FOLLOWING = 'F'
    PENDING = 'P'
    FOLLOW_STATUSES = [
        (FOLLOWING, 'Following'),
        (PENDING, 'Pending'),
    ]

    follower = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
    followee = models.ForeignKey(User, related_name="followers", on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=FOLLOW_STATUSES, default=PENDING)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followee')

class Notification(models.Model):
    # Types of notifications
    FOLLOW_REQUEST = 'FR'
    FOLLOW_ACCEPTED = 'FA'
    NOTIFICATION_TYPES = [
        (FOLLOW_REQUEST, 'Follow Request'),
        (FOLLOW_ACCEPTED, 'Follow Accepted'),
    ]

    to_user = models.ForeignKey(User, related_name='notifications_to', on_delete=models.CASCADE)
    from_user = models.ForeignKey(User, related_name='notifications_from', on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=2, choices=NOTIFICATION_TYPES)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField(default='', blank=True)

    def __str__(self):
        return f'From {self.from_user.username} to {self.to_user.username} - {self.get_notification_type_display()}'