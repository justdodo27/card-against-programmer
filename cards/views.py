from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from rest_framework.viewsets import ViewSet
from .models import Deck, Card, User, Category
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

class DeckViewSet(ViewSet):

    def create(self, request, format=None):
        serializer = DeckSerializer(data=request.data)
        author_id = request.data.pop('author')
        author_instance = User.objects.get(id=author_id)
        categories_ids = request.data.pop('categories')
        categories_instances = Category.objects.filter(id__in=categories_ids)
        cards_data = request.data.pop('cards')
        if not serializer.is_valid():
            raise APIException(f"ERROR : {serializer.errors}")
        else:
            deck = serializer.save(author=author_instance, categories=categories_instances)
            for card in cards_data:
                Card.objects.create(deck=deck, **card)
            return Response(serializer.data)