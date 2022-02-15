from django.urls import path
from cards.models import Deck
from .views import Decks, Cards, DeckID, DeckViewSet

app_name = 'cards'

urlpatterns = [
    path('deck/all', Decks.as_view(), name='decks'), # delete later
    path('card', Cards.as_view(), name='cards'),
    path('deck/<int:id>', DeckID.as_view(), name='deck'),
    path('deck', DeckViewSet.as_view({'post': 'create'}), name='deck - create') # create deck based on request data
]