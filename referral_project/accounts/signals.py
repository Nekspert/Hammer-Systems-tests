import random
import string

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile, User


def generate_invite_code():
    values = string.digits + string.ascii_lowercase
    return ''.join(random.choices(values, k=6))


@receiver(post_save, sender=User)
def create_profile_and_invite_code(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        code = generate_invite_code()
        while Profile.objects.filter(invite_code=code).exists():
            code = generate_invite_code()
        profile.invite_code = code
        profile.save()
