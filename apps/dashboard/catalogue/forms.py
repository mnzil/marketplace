from django import forms

from oscar.core.loading import get_model
from oscar.apps.dashboard.catalogue.forms import ProductClassSelectForm as CoreProductClassSelectForm

ProductClass = get_model('catalogue', 'ProductClass')


class ProductClassSelectForm(CoreProductClassSelectForm):
    """
    Form which is used before creating a product to select it's product class
    """

    def __init__(self, request=None, *args, **kwargs):
        """
        If there's only one product class, pre-select it
        """
        super(ProductClassSelectForm, self).__init__(*args, **kwargs)

        if request is not None:
            print request.user.partners.all().values_list('shop_id', flat=True)
            qs = self.fields['product_class'].queryset = ProductClass.objects.filter(
                shop_id__in=request.user.partners.all().values_list('shop_id', flat=True))

            if not kwargs.get('initial') and len(qs) == 1:
                self.fields['product_class'].initial = qs[0]
        else:
            qs = self.fields['product_class'].queryset = ProductClass.objects.none()


class ProductClassForm(forms.ModelForm):

    class Meta:
        model = ProductClass
        fields = ['name', 'requires_shipping', 'track_stock', 'options']
