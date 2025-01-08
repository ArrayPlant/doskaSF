from django.contrib import admin
from .models import Announcement, Response
from .models import Newsletter

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_at')
    list_filter = ('category', 'author')
    search_fields = ('title', 'content')

@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('announcement', 'user', 'is_accepted', 'created_at')
    list_filter = ('is_accepted', 'created_at')
    search_fields = ('text',)

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('subject', 'created_at')
