# import re

# from django import forms
# from django.db.models import Q
# from django.utils.translation import ugettext_lazy as _
# from oscar.apps.dashboard.ranges.forms import \
#     RangeProductForm as CoreRangeProductForm

# from oscar.core.loading import get_model

# Product = get_model('catalogue', 'Product')


# class RangeProductForm(CoreRangeProductForm):
#     def __init__(self, range, *args, **kwargs):
#         self.shop_id = kwargs.pop('shop_id', None)
#         self.new_range = kwargs.pop('new_range', None)
#         super(RangeProductForm, self).__init__(range, *args, **kwargs)

#     def clean_query(self):
#         raw = self.cleaned_data['query']
#         if not raw:
#             return raw
#         ids = set(re.compile(r'[\w-]+').findall(raw))
#         shop_id = self.shop_id
#         all_products = self.new_range.all_products()
#         print all_products
#         products = all_products.filter(product_class__shop_id=shop_id)
#         existing_skus = set(products.values_list(
#             'stockrecords__partner_sku', flat=True))
#         existing_upcs = set(products.values_list('upc', flat=True))
#         existing_ids = existing_skus.union(existing_upcs)
#         new_ids = ids - existing_ids
#         print new_ids

#         if len(new_ids) == 0:
#             raise forms.ValidationError(
#                 _("The products with SKUs or UPCs matching %s are already in"
#                   " this range") % (', '.join(ids)))

#         self.products = Product._default_manager.filter(
#             Q(stockrecords__partner_sku__in=new_ids) |
#             Q(upc__in=new_ids)).filter(product_class__shop_id=self.shop_id)
#         print self.products
#         if len(self.products) == 0:
#             raise forms.ValidationError(
#                 _("No products exist with a SKU or UPC matching %s")
#                 % ", ".join(ids))

#         found_skus = set(self.products.values_list(
#             'stockrecords__partner_sku', flat=True))
#         found_upcs = set(self.products.values_list('upc', flat=True))
#         found_ids = found_skus.union(found_upcs)
#         self.missing_skus = new_ids - found_ids
#         self.duplicate_skus = existing_ids.intersection(ids)

#         return raw
