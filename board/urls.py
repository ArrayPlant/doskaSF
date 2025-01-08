from django.urls import path
from .views import (
    create_announcement, edit_announcement, my_advertisements, detail_announcement,
    responses_dashboard, delete_response, accept_response
)

urlpatterns = [
    path('create/', create_announcement, name='create_ad'),
    path('my_ads/', my_advertisements, name='my_ads'),
    path('<int:pk>/edit/', edit_announcement, name='edit_ad'),
    path('<int:pk>/', detail_announcement, name='detail_ad'),

    path('responses/', responses_dashboard, name='responses_dashboard'),
    path('responses/<int:pk>/delete/', delete_response, name='delete_response'),
    path('responses/<int:pk>/accept/', accept_response, name='accept_response'),
]
