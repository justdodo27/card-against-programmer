from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters, permissions
from .models import Deck, Card, Category
from .serializers import CategorySerializer, DeckSerializer, CardSerializer, DeckListSerializer
from .pagination import SmallResultsSetPagination, LargeResultsSetPagination

class CardsList(generics.ListCreateAPIView):
    permission_classes = []
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    pagination_class = LargeResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['content']
    search_fields = ['content']
    ordering = ['content']

class CardsDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = []
    queryset = Card.objects.all()
    serializer_class = CardSerializer

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

class CategoryList(generics.ListCreateAPIView):
    permission_classes = []
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['name']
    search_fields = ['name']
    ordering = ['name']

class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = []
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class DecksList(generics.ListCreateAPIView):
    permission_classes = []
    queryset = Deck.objects.all()
    pagination_class = SmallResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['name', 'date_created', 'date_updated']
    search_fields = ['name', 'author__username']
    ordering = ['date_updated', 'name']

    def get_queryset(self):
        queryset = Deck.objects.all()
        name = self.request.query_params.get('name')
        if name is not None:
            queryset.filter(name__icontains=name)
        categories = self.request.query_params.get('categories')
        if categories is not None:
            queryset.filter(categories__id__in=categories)
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return DeckSerializer
        return DeckListSerializer

class DecksDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = []
    queryset = Deck.objects.all()
    serializer_class = DeckSerializer

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)