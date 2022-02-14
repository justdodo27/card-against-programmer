from django.urls import path
from cards.models import Deck
from .views import Decks, Cards, DeckID

app_name = 'cards'

urlpatterns = [
    path('deck', Decks.as_view(), name='decks'),
    path('card', Cards.as_view(), name='cards'),
    path('deck/<int:id>', DeckID.as_view(), name='deck')
]