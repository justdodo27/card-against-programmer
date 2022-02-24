from django.db import models
from django.utils.translation import gettext_lazy as _
from cards.models import Card, Deck
from django.utils.crypto import get_random_string


class Expired(models.Model):
    expire_date = models.DateTimeField(verbose_name=_("Expire Date"), auto_now=True)

    class Meta:
        abstract = True

class Player(Expired):
    class Meta:
        verbose_name = _('Player')
        verbose_name_plural = _('Players')
        ordering = ['id']

    username = models.CharField(max_length=20)
    password = models.CharField(max_length=128)
    hand = models.JSONField(null=True)

    def __str__(self) -> str:
        return self.username

class Game(Expired):
    class Meta:
        verbose_name = _("Game")
        verbose_name_plural = _("Games")
        ordering = ['id']

    code = models.CharField(max_length=8, verbose_name=_('Game Code'), default=get_random_string(length=8), unique=True)
    name = models.CharField(max_length=60, verbose_name=_('Game Name'), default="New Game")
    password = models.CharField(max_length=128, verbose_name=_('Game Password'), null=True)
    creator = models.ForeignKey(Player, default=None, null=True, related_name='game_created', on_delete=models.SET_NULL)
    players = models.ManyToManyField(Player)
    master = models.ForeignKey(Player, default=None, null=True, related_name='game_master', on_delete=models.SET_NULL)
    cards = models.JSONField(null=True)
    cards_stack = models.JSONField(null=True)
    used_stack = models.JSONField(null=True)
    current_question = models.JSONField(null=True)

    def __str__(self) -> str:
        return self.name