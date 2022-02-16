from django.urls import path
from .views import CardsList, CardsDetail, CategoryList, CategoryDetail, DecksList, DecksDetail

app_name = 'cards'

urlpatterns = [
    path('cards/', CardsList.as_view()),
    path('cards/<int:pk>/', CardsDetail.as_view()),
    path('categories/', CategoryList.as_view()),
    path('categories/<int:pk>/', CategoryDetail.as_view()),
    path('decks/', DecksList.as_view()),
    path('decks/<int:pk>/', DecksDetail.as_view()),
]