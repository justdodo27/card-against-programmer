from rest_framework import serializers
from .models import Deck, Category, Card, User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'name'
        ]

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username'
        ]

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = [
            'content',
            'type'
        ]

class DeckSerializer(serializers.ModelSerializer):

    categories = CategorySerializer(many=True, read_only=True)
    author = AuthorSerializer(many=False, read_only=True)
    card = CardSerializer(many=True, read_only=True)

    class Meta:
        model = Deck
        fields = [
            'name',
            'description',
            'categories',
            'date_created',
            'mature_content',
            'author',
            'card'
        ]