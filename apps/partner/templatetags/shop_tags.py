from django import template

from oscar.core.loading import get_model

register = template.Library()
Shop = get_model('partner', 'Shop')


@register.assignment_tag(name="shop_tree")
def get_annotated_list(depth=None, parent=None):
    all_shops = Shop.objects.all()

    return all_shops
