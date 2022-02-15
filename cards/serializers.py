from rest_framework import serializers
from .models import Deck, Category, Card, User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'name'
        ]

    def create(self, validated_data):
        category = Category.objects.create(**validated_data)
        return category

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
        extra_kwargs = {
            'deck': {'allow_null': False, 'required': True},
        }

    def create(self, validated_data):
        card = Card.objects.create(**validated_data)
        return card

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
        extra_kwargs = {
            'author': {'allow_null': False, 'required': True},
            'categories': {'allow_null': True, 'required': False, 'allow_blank': True}
        }

    def create(self, validated_data):
        categories = validated_data.pop("categories")
        deck = Deck.objects.create(**validated_data)
        deck.categories.set(categories)
        return deck