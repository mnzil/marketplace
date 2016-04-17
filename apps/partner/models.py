from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy

from oscar.apps.partner.abstract_models import AbstractPartner
from oscar.models.fields import AutoSlugField


class Shop(models.Model):
    code = AutoSlugField(_("Code"), max_length=128, unique=True,
                         populate_from='title')
    title = models.CharField(
        pgettext_lazy(u"Shop's name", u"Name"), max_length=128, blank=True)


class Partner(AbstractPartner):
    shop = models.ForeignKey(Shop)


from oscar.apps.partner.models import *  # noqa
