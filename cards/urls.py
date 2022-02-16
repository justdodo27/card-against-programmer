from django.urls import path
from cards.models import Deck
from .views import Decks, Cards, DeckID, DeckViewSet, CardViewSet, CategoryViewSet

app_name = 'cards'

urlpatterns = [
    path('deck/all', Decks.as_view(), name='decks'), # delete later
    path('card/all', Cards.as_view(), name='cards'),
    path('card', CardViewSet.as_view({'post': 'create'}), name='card - create'),
    path('deck/<int:id>', DeckID.as_view(), name='deck'),
    path('deck', DeckViewSet.as_view({'post': 'create'}), name='deck - create'),
    path('category', CategoryViewSet.as_view({'post': 'create'}), name='category - create'),
    path('category/<int:pk>', CategoryViewSet.as_view({'put': 'update'}), name='category - update'),
]