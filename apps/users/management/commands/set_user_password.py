from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Changes a user\'s password.'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='The email of the user whose password to change.')
        parser.add_argument('password', type=str, help='The new password.')

    def handle(self, *args, **options):
        email = options['email']
        password = options['password']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise CommandError(f'User with email "{email}" does not exist.')

        user.set_password(password)
        user.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully changed password for user "{email}"'))
