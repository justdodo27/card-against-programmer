from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Updated(models.Model):
    date_updated = models.DateTimeField(
        verbose_name=_("Last Updated"), auto_now=True
    )

    class Meta:
        abstract = True

class Category(models.Model):
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique category name')
        ]

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Deck(Updated):

    class Meta:
        verbose_name = _("Deck")
        verbose_name_plural = _("Decks")
        ordering = ['id']

    name = models.CharField(max_length=255, default=_('New Deck'), verbose_name=_('Deck Name'))
    description = models.TextField(verbose_name=_('Deck Description'))
    categories = models.ManyToManyField(Category)
    date_created = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Date Created')
    )
    mature_content = models.BooleanField(
        default=False, verbose_name=_('Mature Content')
    )
    author = models.ForeignKey(
        User, default=0, related_name='deck', on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

class Card(Updated):

    class Meta:
        verbose_name = _('Card')
        verbose_name_plural = _('Cards')
        ordering = ['id']

    TYPE = (
        (0, _('White')),
        (1, _('Black'))
    )

    deck = models.ForeignKey(
        Deck, related_name='card', on_delete=models.CASCADE
    )
    content = models.CharField(max_length=255, verbose_name=_('Content'))
    type = models.IntegerField(
        choices=TYPE, default=0, verbose_name=_('Type of Card')
    )

    def __str__(self):
        return self.content