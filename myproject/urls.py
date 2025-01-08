from django.contrib import admin
from django.urls import path
from django.urls import include

from .views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('board/', include(('board.urls', 'board'), namespace='board')),
]
