import time

from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError
from psycopg2 import OperationalError as Psycopg2OpError


class Command(BaseCommand):
    help = "Django command to wait for the database to be available"

    def handle(self, *args, **options):
        self.stdout.write("Waiting for database...")
        db_conn = None
        retries = 0
        max_retries = 10

        while not db_conn and retries < max_retries:
            try:
                db_conn = connections["default"]
                db_conn.cursor()  # Try to execute a simple query
                self.stdout.write(self.style.SUCCESS("✅ PostgreSQL Database available!"))
                break
            except (Psycopg2OpError, OperationalError) as e:
                retries += 1
                if retries == max_retries:
                    self.stdout.write(
                        self.style.ERROR(f"❌ PostgreSQL Connection Failed after {max_retries} attempts: {e}")
                    )
                    raise
                self.stdout.write(self.style.WARNING(f"⚠️ Connection Failed! Retrying... ({retries}/{max_retries})"))
                time.sleep(1)
