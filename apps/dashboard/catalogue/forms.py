from django import forms
from django.utils.translation import ugettext_lazy as _

from oscar.core.loading import get_class, get_model

Product = get_model('catalogue', 'Product')
ProductClass = get_model('catalogue', 'ProductClass')
ProductAttribute = get_model('catalogue', 'ProductAttribute')
Category = get_model('catalogue', 'Category')
StockRecord = get_model('partner', 'StockRecord')
ProductCategory = get_model('catalogue', 'ProductCategory')
ProductImage = get_model('catalogue', 'ProductImage')
ProductRecommendation = get_model('catalogue', 'ProductRecommendation')
ProductSelect = get_class('dashboard.catalogue.widgets', 'ProductSelect')


class ProductClassSelectForm(forms.Form):
    """
    Form which is used before creating a product to select it's product class
    """

    product_class = forms.ModelChoiceField(
        label=_("Create a new product of type"),
        empty_label=_("-- Choose type --"),
        queryset=ProductClass.objects.all()
    )

    def __init__(self, request, *args, **kwargs):
        """
        If there's only one product class, pre-select it
        """
        super(ProductClassSelectForm, self).__init__(*args, **kwargs)

        qs = self.fields['product_class'].queryset = ProductClass.objects.filter(
            partner_id__in=request.user.partners.all().values_list('id', flat=True))

        if not kwargs.get('initial') and len(qs) == 1:
            self.fields['product_class'].initial = qs[0]


class ProductClassForm(forms.ModelForm):

    class Meta:
        model = ProductClass
        fields = ['name', 'requires_shipping', 'track_stock', 'options']