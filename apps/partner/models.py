from django.conf import settings
from django.db import models
from django.db.models import Count, Sum
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy
from django.utils.functional import cached_property

from oscar.apps.partner.abstract_models import AbstractPartner
from oscar.apps.catalogue.abstract_models import MissingProductImage
from oscar.models.fields import AutoSlugField


class Shop(models.Model):
    code = AutoSlugField(_("Code"), max_length=128, unique=True,
                         populate_from='title')
    title = models.CharField(
        pgettext_lazy(u"Shop's name", u"Name"), max_length=128, blank=True)
    image = models.ImageField(("image"), upload_to=settings.OSCAR_IMAGE_FOLDER, max_length=255, blank=True)
    description = models.TextField(_('Description'), blank=True)

    def get_absolute_url(self):
        url = reverse(
            'catalogue:shop',
            kwargs={'shop_slug': self.code})
        return url

    def get_missing_image(self):
        return MissingProductImage()

    @property
    def primary_image(self):
        if self.image == 0 or self.image == "":
            return self.get_missing_image()
        return self.image

    def __str__(self):
        return self.title

    def update_rating(self):
        """
        Recalculate rating field
        """
        self.rating = self.calculate_rating()
        self.save()
    update_rating.alters_data = True

    def calculate_rating(self):
        result = self.shopreviews.filter(
            status=self.shopreviews.model.APPROVED
        ).aggregate(
            sum=Sum('score'), count=Count('id'))
        shopreviews_sum = result['sum'] or 0
        shopreviews_count = result['count'] or 0
        rating = None
        if shopreviews_count > 0:
            rating = float(shopreviews_sum) / shopreviews_count
        return rating

    def has_review_by(self, user):
        if user.is_anonymous():
            return False
        return self.shopreviews.filter(user=user).exists()

    def is_review_permitted(self, user):
        if user.is_authenticated() or settings.OSCAR_ALLOW_ANON_REVIEWS:
            return not self.has_review_by(user)
        else:
            return False

    @cached_property
    def num_approved_reviews(self):
        return self.shopreviews.filter(
            status=self.shopreviews.model.APPROVED).count()


class Partner(AbstractPartner):
    shop = models.ForeignKey(Shop)


from oscar.apps.partner.models import *  # noqa
