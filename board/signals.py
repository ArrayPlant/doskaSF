from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

from django.contrib.auth import get_user_model
User = get_user_model()

from .models import Newsletter

@receiver(post_save, sender=Newsletter)
def send_newsletter_to_all_users(sender, instance, created, **kwargs):
    if created:
        all_users = User.objects.all()

        subject = instance.subject
        body = instance.body

        for user in all_users:
            send_mail(
                subject=subject,
                message=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=True,
            )
