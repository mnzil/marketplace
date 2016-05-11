from django.contrib import messages
from django.core.paginator import InvalidPage
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView

from oscar.core.loading import get_class, get_model

Shop = get_model('partner', 'Shop')
Category = get_model('catalogue', 'category')
get_product_search_handler_class = get_class(
    'catalogue.search_handlers', 'get_product_search_handler_class')


class ProductShopView(TemplateView):
    """
    Browse products in a given shop
    """
    context_object_name = "products"
    template_name = 'catalogue/shop.html'
    enforce_paths = True

    def get(self, request, *args, **kwargs):
        self.shop = self.get_shop()
        self.category = self.get_category()
        if self.shop is None and self.category is None:
            raise Http404
        try:
            self.search_handler = self.get_search_handler(
                request.GET, request.get_full_path(), categories=self.get_categories(), shop=self.shop)
        except InvalidPage:
            messages.error(request, _('The given page number was invalid.'))
            return redirect(self.category.get_absolute_url())

        return super(ProductShopView, self).get(request, *args, **kwargs)

    def get_shop(self):
        if 'shop_slug' in self.kwargs:
            return get_object_or_404(Shop, code=self.kwargs['shop_slug'])
        return None

    def get_category(self):
        if 'category_slug' in self.kwargs:
            concatenated_slugs = self.kwargs['category_slug']
            slugs = concatenated_slugs.split(Category._slug_separator)
            try:
                last_slug = slugs[-1]
            except IndexError:
                return None
            else:
                for category in Category.objects.filter(slug=last_slug):
                    if category.full_slug == concatenated_slugs:
                        return category

        return None

    def get_search_handler(self, *args, **kwargs):
        return get_product_search_handler_class()(*args, **kwargs)

    def get_categories(self):
        """
        Return a list of the current category and its ancestors
        """
        if self.category is not None:
            return self.category.get_descendants_and_self()
        return None

    def get_context_data(self, **kwargs):
        context = super(ProductShopView, self).get_context_data(**kwargs)
        context['shop'] = self.shop
        try:
            context['category'] = self.category
        except:
            pass
        search_context = self.search_handler.get_search_context_data(self.context_object_name)
        context.update(search_context)
        return context
