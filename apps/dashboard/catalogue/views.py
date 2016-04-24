from django.http import HttpResponseRedirect
from oscar.apps.dashboard.catalogue.views import \
    ProductListView as CoreProductListView, \
    ProductCreateRedirectView as CoreProductCreateRedirectView,  \
    ProductClassCreateUpdateView as CoreProductClassCreateUpdateView, \
    ProductClassCreateView as CoreProductClassCreateView, \
    ProductClassListView as CoreProductClassListView, \
    ProductCreateUpdateView as CoreProductCreateUpdateView, \
    ProductDeleteView as CoreProductDeleteView
from oscar.core.loading import get_model

Product = get_model('catalogue', 'Product')


def filter_products(queryset, user):
    shop_id = user.partners.all().values_list(
        'shop_id',
        flat=True)[0]
    queryset = queryset.filter(product_class__shop_id=shop_id).distinct()
    return queryset


class ProductListView(CoreProductListView):
    def get_context_data(self, **kwargs):
        ctx = super(ProductListView, self).get_context_data(**kwargs)
        ctx['form'] = self.form
        ctx['new_productclass_form'] = self.productclass_form_class(
            request=self.request)
        return ctx

    def filter_queryset(self, queryset):
        return filter_products(queryset, self.request.user)


class ProductClassListView(CoreProductClassListView):
    def get_queryset(self):
        return super(ProductClassListView, self).get_queryset().filter(
            shop_id=self.request.shop_id)


class ProductCreateRedirectView(CoreProductCreateRedirectView):
    def get_redirect_url(self, **kwargs):
        form = self.productclass_form_class(self.request, self.request.GET)
        if form.is_valid():
            product_class = form.cleaned_data['product_class']
            return self.get_product_create_url(product_class)

        else:
            return self.get_invalid_product_class_url()


class ProductClassCreateUpdateView(CoreProductClassCreateUpdateView):
    def forms_valid(self, form, attributes_formset):
        up_form = form.save(commit=False)
        up_form.shop_id = self.request.shop_id
        up_form.save()
        attributes_formset.save()

        return HttpResponseRedirect(self.get_success_url())


class ProductClassCreateView(
        ProductClassCreateUpdateView,
        CoreProductClassCreateView):
    pass


class ProductCreateUpdateView(CoreProductCreateUpdateView):
    def get_queryset(self):
        return filter_products(Product.objects.all(), self.request.user)


class ProductDeleteView(CoreProductDeleteView):
    def get_queryset(self):
        return filter_products(Product.objects.all(), self.request.user)
