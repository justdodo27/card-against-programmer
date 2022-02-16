from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from rest_framework.viewsets import ViewSet
from .models import Deck, Card, User, Category
from .serializers import CategorySerializer, DeckSerializer, CardSerializer

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

    def update(self, request, pk=None):
        deck_instance = Deck.objects.get(id=pk)
        serializer = DeckSerializer(deck_instance, data=request.data)
        categories_ids = request.data.pop('categories')
        categories_instances = Category.objects.filter(id__in=categories_ids)
        if not serializer.is_valid():
            raise APIException(f"ERROR : {serializer.errors}")
        else:
            serializer.save(categories=categories_instances)
            return Response(serializer.data)

class CardViewSet(ViewSet):

    def create(self, request, format=None):
        serializer = CardSerializer(data=request.data)
        deck_id = request.data.pop('deck')
        deck_instance = Deck.objects.get(id=deck_id)
        if not serializer.is_valid():
            raise APIException(f"ERROR : {serializer.errors}")
        else:
            serializer.save(deck=deck_instance)
            return Response(serializer.data)

    def update(self, request, pk=None):
        card_instance = Card.objects.get(id=pk)
        serializer = CardSerializer(card_instance, data=request.data)
        if not serializer.is_valid():
            raise APIException(f"ERROR : {serializer.errors}")
        else:
            serializer.save()
            return Response(serializer.data)

class CategoryViewSet(ViewSet):

    def create(self, request, format=None):
        serializer = CategorySerializer(data=request.data)
        if not serializer.is_valid():
            raise APIException(f"ERROR : {serializer.errors}")
        else:
            serializer.save()
            return Response(serializer.data)
    
    def update(self, request, pk=None):
        category_instance = Category.objects.get(id=pk)
        serializer = CategorySerializer(category_instance, data=request.data)
        if not serializer.is_valid():
            raise APIException(f"ERROR : {serializer.errors}")
        else:
            serializer.save()
            return Response(serializer.data)