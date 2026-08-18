from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
import os


class Command(BaseCommand):
    help = "Create Render superuser"

    def handle(self, *args, **kwargs):
         # Create groups
        Group.objects.get_or_create(name="Vendor")
        Group.objects.get_or_create(name="Supplier")

        self.stdout.write(
            self.style.SUCCESS("Vendor and Supplier groups are ready.")
        )

        User = get_user_model()

        username = os.environ.get("ADMIN_USERNAME", "bhanu")
        email = os.environ.get("ADMIN_EMAIL", "bhanu@gmail.com")
        password = os.environ.get("bhanu@123")

        if not password:
            self.stdout.write(
                self.style.ERROR("ADMIN_PASSWORD environment variable is missing.")
            )
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write("Admin user already exists.")
            return

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )

        self.stdout.write(
            self.style.SUCCESS("Superuser created successfully.")
        )