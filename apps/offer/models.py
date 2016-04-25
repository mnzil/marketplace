from django.db import models
from oscar.apps.offer.abstract_models import AbstractRange
from oscar.apps.offer.abstract_models import AbstractConditionalOffer
from oscar.core.loading import get_model

Shop = get_model('partner', 'Shop')


class Range(AbstractRange):
    shop = models.ForeignKey(Shop)


class ConditionalOffer(AbstractConditionalOffer):
    shop = models.ForeignKey(Shop)


from oscar.apps.offer.models import *  # noqa
