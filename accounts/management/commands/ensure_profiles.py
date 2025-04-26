from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Profile

class Command(BaseCommand):
    help = 'Ensures every user has a profile'

    def handle(self, *args, **options):
        users_without_profiles = User.objects.filter(profile__isnull=True)
        for user in users_without_profiles:
            Profile.objects.create(user=user)
            self.stdout.write(self.style.SUCCESS(f'Profile created for {user.username}'))

        self.stdout.write(self.style.SUCCESS('Completed ensuring all users have profiles.'))