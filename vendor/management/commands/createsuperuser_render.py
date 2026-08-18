from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
import os


class Command(BaseCommand):
    help = "Create Render groups and admin user"

    def handle(self, *args, **kwargs):

        # Create required groups
        Group.objects.get_or_create(name="Vendor")
        Group.objects.get_or_create(name="Supplier")

        self.stdout.write(
            self.style.SUCCESS("Vendor and Supplier groups are ready.")
        )

        User = get_user_model()

        username = os.environ.get("ADMIN_USERNAME", "admin")
        email = os.environ.get(
            "ADMIN_EMAIL",
            "admin@example.com"
        )
        password = os.environ.get("ADMIN_PASSWORD")

        if not password:
            self.stdout.write(
                self.style.ERROR("ADMIN_PASSWORD is missing.")
            )
            return

        user, created = User.objects.get_or_create(
            username=username,
            defaults={"email": email}
        )

        if created:
            user.set_password(password)

        user.email = email
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()

        self.stdout.write(
            self.style.SUCCESS(
                f"Admin privileges enabled for {username}."
            )
        )