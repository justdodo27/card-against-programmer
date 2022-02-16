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

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance

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

    def update(self, instance, validated_data):
        instance.content = validated_data.get('content', instance.content)
        instance.type = validated_data.get('type', instance.type)
        instance.save()
        return instance

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
            'date_updated',
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

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.mature_content = validated_data.get('mature_content', instance.mature_content)
        categories = validated_data.pop('categories')
        instance.categories.set(categories)
        instance.save()
        return instance