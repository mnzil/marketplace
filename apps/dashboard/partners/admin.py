from django.contrib import admin
from oscar.core.loading import get_model

Shop = get_model('partner', 'Shop')

admin.site.register(Shop)
from oscar.apps.partner.admin import *  # noqa
