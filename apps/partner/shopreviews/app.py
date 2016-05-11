from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from oscar.core.application import Application
from oscar.core.loading import get_class


class ShopReviewsApplication(Application):
    name = None
    hidable_feature_name = "shopreviews"

    detail_view = get_class('partner.shopreviews.views', 'ShopReviewDetail')
    create_view = get_class('partner.shopreviews.views', 'CreateShopReview')
    vote_view = get_class('partner.shopreviews.views', 'AddVoteView')
    list_view = get_class('partner.shopreviews.views', 'ShopReviewList')

    def get_urls(self):
        urls = [
            url(r'^(?P<pk>\d+)/$', self.detail_view.as_view(),
                name='shopreviews-detail'),
            url(r'^add/$', self.create_view.as_view(),
                name='shopreviews-add'),
            url(r'^(?P<pk>\d+)/vote/$',
                login_required(self.vote_view.as_view()),
                name='shopreviews-vote'),
            url(r'^$', self.list_view.as_view(), name='shopreviews-list'),
        ]
        return self.post_process_urls(urls)


application = ShopReviewsApplication()
