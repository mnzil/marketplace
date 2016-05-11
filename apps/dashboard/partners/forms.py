from django import forms
from oscar.core.loading import get_model
Shop = get_model('partner', 'Shop')


class ShopDetailsForm(forms.ModelForm):
    class Meta:
        exclude = []
        model = Shop
