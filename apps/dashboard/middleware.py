class ShopMiddleware(object):
    def process_request(self, request):
        if request.user and request.user.is_authenticated():
            shop_id = request.user.partners.all().values_list(
                'shop_id',
                flat=True)
            if shop_id:
                request.shop_id = shop_id[0]
            else:
                request.shop_id = -1
        else:
            request.shop_id = -1
        return
