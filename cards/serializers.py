from multiprocessing import managers
from rest_framework import serializers
from .models import Deck, Category, Card, User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
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
            'id',
            'username'
        ]

class CardDeckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = [
            'id',
            'content',
            'type'
        ]

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = [
            'id',
            'content',
            'type',
            'deck'
        ]
        extra_kwargs = {
            'deck': {'allow_null': False, 'required': True},
        }

    def validate(self, data):
        """
        Check that content and type 
        """
        user_id = self.context['request'].user.id
        method = self.context['request'].method
        if method in ['PUT', 'DELETE'] and user_id != self.instance.deck.author.id:
            raise serializers.ValidationError("you are not the author")
        if data['type'] == 0 and '_' in data['content']:
            raise serializers.ValidationError("card of type white (0) cannot have underscores")
        if data['type'] == 1 and '_' not in data['content']:
            raise serializers.ValidationError("card of type black (1) must have at least one underscore")
        if data['type'] not in (0,1):
            raise serializers.ValidationError("wrong type")
        return data

    def create(self, validated_data):
        card = Card.objects.create(**validated_data)
        return card

    def update(self, instance, validated_data):
        instance.content = validated_data.get('content', instance.content)
        instance.type = validated_data.get('type', instance.type)
        instance.save()
        return instance

class DeckListSerializer(serializers.ModelSerializer):
    card = CardDeckSerializer(many=True)
    author = AuthorSerializer(many=False, read_only=True)
    categories = CategorySerializer(many=True)

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

class DeckSerializer(serializers.ModelSerializer):
    card = CardDeckSerializer(many=True)

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
            'categories': {'allow_null': True, 'required': False, 'many': True, 'allow_empty': True}
        }

    def validate(self, data):
        """
        Check that content and type 
        """
        user_id = self.context['request'].user.id
        method = self.context['request'].method
        if method in ['PUT', 'DELETE'] and user_id != self.instance.author.id:
            raise serializers.ValidationError("you are not the author")
        
        return data

    def create(self, validated_data):
        categories = validated_data.pop("categories")
        card_data = validated_data.pop("card")
        deck = Deck.objects.create(**validated_data)
        deck.categories.set(categories)
        for card in card_data:
            Card.objects.create(deck=deck, **card)
        return deck

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.mature_content = validated_data.get('mature_content', instance.mature_content)
        categories = validated_data.pop('categories')
        instance.categories.set(categories)
        instance.save()
        return instance