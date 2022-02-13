from django.urls import path
from .views import Card

app_name = 'cards'

urlpatterns = [
    path('', Card.as_view(), name='card'),
]