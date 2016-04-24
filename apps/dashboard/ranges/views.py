from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from oscar.apps.dashboard.ranges.views import \
    RangeListView as CoreRangeListView, \
    RangeCreateView as CoreRangeCreateView, \
    RangeUpdateView as CoreRangeUpdateView, \
    RangeDeleteView as CoreRangeDeleteView, \
    RangeProductListView as CoreRangeProductListView
from oscar.core.loading import get_model

Range = get_model('offer', 'Range')


def filter_ranges(queryset, user):
    try:
        shop_id = user.partners.all().values_list(
            'shop_id',
            flat=True)[0]
        queryset = queryset.filter(shop_id=shop_id).distinct()
    except:
        queryset = queryset.none()
    return queryset


class RangeListView(CoreRangeListView):
    def get_queryset(self):
        return super(RangeListView, self).get_queryset().filter(
            shop_id=self.request.shop_id)


class RangeCreateView(CoreRangeCreateView):
    def form_valid(self, form):
        form.instance.shop_id = self.request.shop_id
        form.instance.save()
        return super(RangeCreateView, self).form_valid(form)


class RangeUpdateView(CoreRangeUpdateView):
    def get_object(self):
        self.partner = get_object_or_404(
            Range,
            pk=self.kwargs.get('pk', None),
            shop_id=self.request.shop_id)
        return super(RangeUpdateView, self).get_object()


class RangeDeleteView(CoreRangeDeleteView):
    def get_object(self):
        self.partner = get_object_or_404(
            Range,
            pk=self.kwargs.get('pk', None),
            shop_id=self.request.shop_id)
        return super(RangeDeleteView, self).get_object()


class RangeProductListView(CoreRangeProductListView):
    def add_products(self, request):
        range = self.get_range()
        form = self.form_class(
            range,
            request.POST,
            request.FILES,
            new_range=range,
            shop_id=self.request.shop_id
        )
        if not form.is_valid():
            ctx = self.get_context_data(form=form,
                                        object_list=self.object_list)
            return self.render_to_response(ctx)

        self.handle_query_products(request, range, form)
        self.handle_file_products(request, range, form)
        return HttpResponseRedirect(self.get_success_url(request))



# products = self.get_range().all_products().filter(product_class__shop_id=shop_id)
