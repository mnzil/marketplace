from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ShopReviewsConfig(AppConfig):
    label = 'shopreviews'
    name = 'apps.partner.shopreviews'
    verbose_name = _('Shop reviews')
