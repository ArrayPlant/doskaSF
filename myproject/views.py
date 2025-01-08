from django.shortcuts import render
from board.models import Announcement

def home_view(request):
    announcements = Announcement.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'announcements': announcements})
