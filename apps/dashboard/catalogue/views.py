from oscar.apps.dashboard.catalogue.views import ProductListView as CoreProductListView


class ProductListView(CoreProductListView):
    """
    Dashboard view of the product list.
    Supports the permission-based dashboard.
    """
    def get_context_data(self, **kwargs):
        ctx = super(ProductListView, self).get_context_data(**kwargs)
        ctx['form'] = self.form
        ctx['new_productclass_form'] = self.productclass_form_class(request=self.request)
        return ctx
