from datetime import datetime, timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone_number = models.CharField(
            unique=True, db_index=True, max_length=15, verbose_name='Номер телефона'
    )

    def __str__(self):
        return f'<{self.phone_number}>'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    invite_code = models.CharField(max_length=6, unique=True, db_index=True)
    used_invite = models.ForeignKey(
            'self', null=True, blank=True, on_delete=models.SET_NULL, related_name='referrals'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'<{self.user.username}:{self.invite_code}>'


class PhoneCode(models.Model):
    phone_number = models.CharField(max_length=15, db_index=True)
    code = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return datetime.now() > self.created_at + timedelta(minutes=5)

    def __str__(self):
        return f'<{self.code}>'
