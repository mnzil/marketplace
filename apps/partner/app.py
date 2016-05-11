from django.conf.urls import include, url

from apps.partner.shopreviews.app import application as shopreviews_app
from oscar.core.application import Application


class ShopReviewsApplication(Application):
    name = "shop"
    shopreviews_app = shopreviews_app

    def get_urls(self):
        urlpatterns = super(ShopReviewsApplication, self).get_urls()
        urlpatterns += [
            url(r'^(?P<shop_code>[\w-]*)_(?P<shop_pk>\d+)/reviews/',
                include(self.shopreviews_app.urls)),
        ]
        return self.post_process_urls(urlpatterns)

application = ShopReviewsApplication()
