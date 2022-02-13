from django.contrib import admin
from . import models

@admin.register(models.Category)

class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'name',
    ]


class CardInlineModel(admin.TabularInline):
    model = models.Card
    fields = [
        'content',
        'type',
    ]


@admin.register(models.Deck)

class DeckAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
    ]

    inlines = [
        CardInlineModel,
    ]

@admin.register(models.Card)

class CardAdmin(admin.ModelAdmin):
    list_display = [
        'content'
    ]