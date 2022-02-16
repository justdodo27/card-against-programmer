from django.urls import path
from .views import Decks, Cards, DeckViewSet, CardViewSet, CategoryViewSet

app_name = 'cards'

urlpatterns = [
    path('deck/all', Decks.as_view(), name='decks'), # delete later
    path('card/all', Cards.as_view(), name='cards'),
    path('category', CategoryViewSet.as_view({'post': 'create'}), name='category - create'),
    path('category/<int:pk>', CategoryViewSet.as_view({'put': 'update'}), name='category - update'),
    path('card', CardViewSet.as_view({'post': 'create'}), name='card - create'),
    path('card/<int:pk>', CardViewSet.as_view({'put': 'update'}), name='card - update'),
    path('deck', DeckViewSet.as_view({'post': 'create'}), name='deck - create'),
    path('deck/<int:pk>', DeckViewSet.as_view({'put': 'update'}), name='deck - update'),
]