import time
from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand
from psycopg2 import OperationalError as Psycopg2OpError

class Command(BaseCommand):
    help = "Django command to wait for the database to be available"

    def handle(self, *args, **options):
        """DB가 준비될 때까지 10번 재시도"""
        for i in range(10):
            self.stdout.write(f"Try {i+1}: Waiting for database...")
            try:
                connection = connections["default"]
                connection.cursor()  # 실제 연결 시도
                self.stdout.write(self.style.SUCCESS("✅ PostgreSQL Database available!"))
                return
            except (Psycopg2OpError, OperationalError):
                if i == 9:
                    self.stdout.write(self.style.ERROR("❌ PostgreSQL Connection Failed after 10 attempts"))
                else:
                    self.stdout.write(self.style.WARNING("⚠️ Connection Failed! Retrying..."))
                    time.sleep(1)