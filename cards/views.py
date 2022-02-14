from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Deck, Card
from .serializers import DeckSerializer, CardSerializer

class Decks(generics.ListAPIView):
    serializer_class = DeckSerializer
    queryset = Deck.objects.all()

class Cards(generics.ListAPIView):
    serializer_class = CardSerializer
    queryset = Card.objects.all()

class DeckID(APIView):
    def get(self, request, format=None, **kwargs):
        deck = Deck.objects.get(id=kwargs['id'])
        serializer = DeckSerializer(deck)
        return Response(serializer.data)