from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

User = get_user_model()


class Command(BaseCommand):
    help = "Creates a new superuser non-interactively."

    def add_arguments(self, parser):
        parser.add_argument("--email", type=str, help="The superuser's email address.", required=True)
        parser.add_argument("--password", type=str, help="The superuser's password.", required=True)
        parser.add_argument("--name", type=str, help="The superuser's name.", default="Admin")
        parser.add_argument("--nickname", type=str, help="The superuser's nickname.", default="Admin")

    def handle(self, *args, **options):
        email = options["email"]
        password = options["password"]
        name = options["name"]
        nickname = options["nickname"]

        if User.objects.filter(email=email).exists():
            raise CommandError(f'User with email "{email}" already exists.')

        self.stdout.write(f"Creating superuser {email}...")
        User.objects.create_superuser(email=email, password=password, name=name, nickname=nickname)
        self.stdout.write(self.style.SUCCESS(f'Successfully created superuser "{email}"'))
