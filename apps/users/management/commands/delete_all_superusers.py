from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Deletes all superuser accounts.'

    def handle(self, *args, **options):
        superusers = User.objects.filter(is_superuser=True)
        count = superusers.count()
        if count == 0:
            self.stdout.write(self.style.WARNING('No superusers found to delete.'))
            return

        self.stdout.write(self.style.WARNING(f'Deleting {count} superuser(s)...'))
        superusers.delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted all superuser accounts.'))
