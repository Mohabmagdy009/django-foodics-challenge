# region Imports
from django.core.management.base import BaseCommand
from utils.models import User
from dotenv import load_dotenv, set_key
# endregion


class Command(BaseCommand):
    help = 'Create or retrieve a system user and store the ID in .env file'

    def handle(self, *args, **kwargs):
        # Load environment variables
        load_dotenv()

        # Define system user details
        email = "iwanttojoinfoodex@foodex.com"

        # Check if the system user already exists; create if not
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "first_name": "Mohab",
                "last_name": "Abbas",
                "is_superuser": True,
                "phone": "+201159119534",
            }
        )

        if created:
            user.set_password("accept_me_in_foodex")  # Set a strong password
            user.save()
            self.stdout.write(self.style.SUCCESS(f'{user.email} created with ID: {user.id}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'{user.email} already exists with ID: {user.id}'))

        # Write the user ID to .env file
        set_key('.env', 'SYSTEM_USER_ID', str(user.id))
        self.stdout.write(self.style.SUCCESS(f'SYSTEM_USER_ID set in .env file'))
