from django.core.management.base import BaseCommand

from apps.users.models import CustomUser


class Command(BaseCommand):
    help = "Activates specified user accounts by email."

    def add_arguments(self, parser):
        parser.add_argument("emails", nargs="+", type=str, help="One or more user emails to activate.")

    def handle(self, *args, **options):
        emails = options["emails"]
        activated_count = 0
        for email in emails:
            try:
                user = CustomUser.objects.get(email=email)
                if not user.is_active:
                    user.is_active = True
                    user.save()
                    self.stdout.write(self.style.SUCCESS(f"Successfully activated user: {email}"))
                    activated_count += 1
                else:
                    self.stdout.write(self.style.WARNING(f"User {email} is already active."))
            except CustomUser.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"User with email {email} does not exist."))
        self.stdout.write(self.style.SUCCESS(f"Finished. Activated {activated_count} user(s)."))
