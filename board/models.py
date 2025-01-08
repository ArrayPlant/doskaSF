from django.db import models
from django.contrib.auth import get_user_model

from ckeditor.fields import RichTextField

User = get_user_model()

class Announcement(models.Model):
    CATEGORY_CHOICES = [
        ("tank", "Танки"),
        ("healer", "Хилы"),
        ("dd", "ДД"),
        ("trader", "Торговцы"),
        ("guildmaster", "Гилдмастеры"),
        ("questgiver", "Квестгиверы"),
        ("blacksmith", "Кузнецы"),
        ("leatherworker", "Кожевники"),
        ("alchemist", "Зельевары"),
        ("spellmaster", "Мастера заклинаний"),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="announcements")
    title = models.CharField(max_length=200)
    #content = models.TextField()
    content = RichTextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Response(models.Model):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name="responses")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="responses")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"Отклик от {self.user} на '{self.announcement}'"

class Newsletter(models.Model):
    subject = models.CharField(max_length=200)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject