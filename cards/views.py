from rest_framework import generics
from .models import Deck, Card
from .serializers import DeckSerializer, CardSerializer

class Deck(generics.ListAPIView):
    serializer_class = DeckSerializer
    queryset = Deck.objects.all()

class Card(generics.ListAPIView):
    serializer_class = CardSerializer
    queryset = Card.objects.all()