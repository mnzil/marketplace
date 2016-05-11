from django.conf.urls import url
from oscar.core.loading import get_class
from oscar.apps.dashboard.partners.app import PartnersDashboardApplication as CorePartnersDashboardApplication


class PartnersDashboardApplication(CorePartnersDashboardApplication):
    shop_update_view = get_class('dashboard.partners.views',
                                 'ShopDetailsUpdateView')

    def get_urls(self):
        urls = super(PartnersDashboardApplication, self).get_urls()
        urls += [
            url(r'^shop-details/$', self.shop_update_view.as_view(),
                name='shop-details'),
        ]

        return self.post_process_urls(urls)


application = PartnersDashboardApplication()
