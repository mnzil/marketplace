from django.db import models
from oscar.apps.catalogue.abstract_models import AbstractProductClass
from oscar.core.loading import get_model

Partner = get_model('partner', 'partner')


class ProductClass(AbstractProductClass):
    partner = models.OneToOneField(Partner)

from oscar.apps.catalogue.models import *
