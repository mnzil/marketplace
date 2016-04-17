from oscar.apps.dashboard.catalogue.views import ProductListView as CoreProductListView
from oscar.apps.dashboard.catalogue.views import ProductCreateRedirectView as CoreProductCreateRedirectView


class ProductListView(CoreProductListView):
    def get_context_data(self, **kwargs):
        ctx = super(ProductListView, self).get_context_data(**kwargs)
        ctx['form'] = self.form
        ctx['new_productclass_form'] = self.productclass_form_class(request=self.request)
        return ctx


class ProductCreateRedirectView(CoreProductCreateRedirectView):
    def get_redirect_url(self, **kwargs):
        form = self.productclass_form_class(self.request, self.request.GET)
        if form.is_valid():
            product_class = form.cleaned_data['product_class']
            return self.get_product_create_url(product_class)

        else:
            return self.get_invalid_product_class_url()
