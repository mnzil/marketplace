from oscar.core.decorators import deprecated
from oscar.core.loading import get_model
from oscar.apps.catalogue.search_handlers import \
    SolrProductSearchHandler as CoreSolrProductSearchHandler, \
    ESProductSearchHandler as CoreESProductSearchHandler, \
    SimpleProductSearchHandler as CoreSimpleProductSearchHandler

Product = get_model('catalogue', 'Product')


class SolrProductSearchHandler(CoreSolrProductSearchHandler):
    def __init__(self, request_data, full_path, categories=None, shop=None):
        self.shop = shop
        self.categories = categories
        super(SolrProductSearchHandler, self).__init__(request_data, full_path)

    def get_search_queryset(self):
        sqs = super(SolrProductSearchHandler, self).get_search_queryset()
        if self.categories:
            pattern = ' OR '.join([
                '"%s"' % c.full_name for c in self.categories])
            sqs = sqs.narrow('category_exact:(%s)' % pattern)
        if self.shop:
            sqs = sqs.narrow('product_class__shop_id:(%s)' % self.shop.id)
        return sqs


ProductSearchHandler = deprecated(SolrProductSearchHandler)


class ESProductSearchHandler(CoreESProductSearchHandler):
    def __init__(self, request_data, full_path, categories=None, shop=None):
        self.shop = shop
        self.categories = categories
        super(ESProductSearchHandler, self).__init__(request_data, full_path)

    def get_search_queryset(self):
        sqs = super(ESProductSearchHandler, self).get_search_queryset()
        if self.categories:
            for category in self.categories:
                sqs = sqs.filter_or(category=category.full_name)
        if self.shop:
            sqs = sqs.filter_or(product_class__shop_id=self.shop.id)
        return sqs


class SimpleProductSearchHandler(CoreSimpleProductSearchHandler):
    def __init__(self, request_data, full_path, categories=None, shop=None):
        self.shop = shop
        self.categories = categories
        self.kwargs = {'page': request_data.get('page', 1)}
        self.object_list = self.get_queryset()

    def get_queryset(self):
        qs = Product.browsable.base_queryset()
        if self.categories:
                qs = qs.filter(categories__in=self.categories).distinct()
        if self.shop:
            qs = qs.filter(product_class__shop_id=self.shop.id).distinct()
        return qs

    def get_search_context_data(self, context_object_name):
        # Set the context_object_name instance property as it's needed
        # internally by MultipleObjectMixin
        self.context_object_name = context_object_name
        context = self.get_context_data(object_list=self.object_list)
        context[context_object_name] = context['page_obj'].object_list
        return context
