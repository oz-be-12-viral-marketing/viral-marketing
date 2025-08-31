from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CustomUser


@receiver(post_save, sender=CustomUser)
def create_welcome_message(sender, instance, created, **kwargs):
    if created:
        print(f"New user created: {instance.email} 님이 회원가입하셨습니다!")
