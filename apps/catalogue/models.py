from django.db import models
from oscar.apps.catalogue.abstract_models import AbstractProductClass
from oscar.core.loading import get_model

Shop = get_model('partner', 'Shop')


class ProductClass(AbstractProductClass):
    shop = models.OneToOneField(Shop)

from oscar.apps.catalogue.models import *
