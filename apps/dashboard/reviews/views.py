from oscar.apps.dashboard.reviews.views import ReviewListView as CoreReviewListView


class ReviewListView(CoreReviewListView):
    def get_queryset(self):
        print super(ReviewListView, self).get_queryset().filter(
            product__product_class__shop_id=self.request.shop_id)

        return super(ReviewListView, self).get_queryset().filter(
            product__product_class__shop_id=self.request.shop_id)
