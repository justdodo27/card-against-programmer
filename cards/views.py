from pkg_resources import register_finder


from rest_framework import generics
from .models import Card
from .serializers import CardSerializer

class Card(generics.ListAPIView):
    serializer_class = CardSerializer
    queryset = Card.objects.all()