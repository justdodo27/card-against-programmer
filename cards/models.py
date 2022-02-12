from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Updated(models.Model):
    date_updated = models.DateTimeField(
        verbose_name=_("Last Updated"), auto_now=True
    )

    class Meta:
        abstract = True

class Category(models.Model):
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

    def __str__(self):
        return self.name

class Card(Updated):

    class Meta:
        verbose_name = _('Card')
        verbose_name_plural = _('Cards')
        ordering = ['id']

    deck = models.ForeignKey(
        Deck, related_name='card', on_delete=models.CASCADE
    )
    content = models.CharField(max_length=255, verbose_name=_('Content'))

    def __str__(self):
        return self.content