from django import forms
from django.contrib.auth.models import User

from oscar.apps.customer.utils import normalise_email
from oscar.apps.partner.models import Partner


class GatewayForm(forms.Form):
    email = forms.EmailField()
    shop_name = forms.CharField()

    def clean_email(self):
        email = normalise_email(self.cleaned_data['email'])
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "A user already exists with email %s" % email
            )
        return email

    def clean_shop_name(self):
        shop_name = self.cleaned_data['shop_name']
        if Partner.objects.filter(code__exact=shop_name).exists():
            raise forms.ValidationError(
                "A Shop already exists with this name %s" % shop_name
            )
        return shop_name
