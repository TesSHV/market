from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os


class Command(BaseCommand):
    help = 'Create an admin user if none exists'

    def handle(self, *args, **options):

        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'root')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'root@gmail.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', '1234')

        if User.objects.filter(is_staff=True, is_superuser=True).exists():
            self.stdout.write(self.style.SUCCESS('Admin user already exists.'))
        else:
            admin_user = User.objects.create_user(username, email, password)
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.save()

            self.stdout.write(self.style.SUCCESS('Admin user created successfully.'))