from django.db import models
from django.contrib.auth.models import AbstractUser
import secrets

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_confirmed = models.BooleanField(default=False)
    confirmation_code = models.CharField(max_length=64, blank=True, null=True)

    REQUIRED_FIELDS = ['email']

    def save(self, *args, **kwargs):
        if not self.pk and not self.confirmation_code:
            self.confirmation_code = secrets.token_urlsafe(32)
        super().save(*args, **kwargs)
