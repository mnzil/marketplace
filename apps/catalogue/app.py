from django.conf.urls import url
from oscar.core.loading import get_class
from oscar.core.application import Application
from oscar.apps.catalogue.app import CatalogueApplication as CoreCatalogueApplication


class ShopApplication(Application):
    name = 'shop'
    shop_view = get_class('catalogue.views', 'ProductShopView')

    def get_urls(self):
        urlpatterns = super(ShopApplication, self).get_urls()
        urlpatterns += [
            url(r'^shop/(?P<shop_slug>[\w-]+(/[\w-]+)*)/$',
                self.shop_view.as_view(), name='shop'),
            url(r'^category/(?P<category_slug>[\w-]+(/[\w-]+)*)_(?P<pk>\d+)/(?P<shop_slug>[\w-]+(/[\w-]+)*)/$',
                self.shop_view.as_view()),
        ]
        return self.post_process_urls(urlpatterns)


class CatalogueApplication(CoreCatalogueApplication, ShopApplication):
    """
    Composite class combining Products with Reviews and Shops
    """

application = CatalogueApplication()
