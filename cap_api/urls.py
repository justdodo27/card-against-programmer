from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('cards.urls', namespace='card')),
    path('game/', include('game.urls', namespace='game')),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]
