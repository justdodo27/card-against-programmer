from django.urls import path
from .views import Deck, Card

app_name = 'cards'

urlpatterns = [
    path('deck', Deck.as_view(), name='deck'),
    path('card', Card.as_view(), name='card'),
]